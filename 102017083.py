# -*- coding: utf-8 -*-

"""#pytube is a Python library for downloading videos and audio from YouTube.
# It allows you to interact with YouTube's data and download video or audio streams of a specific video.
#pydub is a Python library for audio processing.
# Import necessary libraries
from pytube import YouTube
from pydub import AudioSegment
#used for opening and reading URLs (Uniform Resource Locators). It allows you to make HTTP requests to retrieve data from web resources,
import urllib.request
#regular expression
import re
#Manipulating file paths and directories (e.g., creating, deleting, renaming files and directories).
import os
#Accessing command-line arguments passed to a Python script.
import sys

# Define the main function
def main():
    # Check the number of command-line arguments
    if len(sys.argv) == 5:
        # Parse command-line arguments
        name = sys.argv[1]
        name = name.replace(' ', '') + "songs"  # Remove spaces and append "songs"
        try:
            no_of_songs = int(sys.argv[2])  # Number of songs to download
            time = int(sys.argv[3])  # Duration (in seconds) for each song
        except:
            sys.exit("Wrong Parameters entered")  # Exit with an error message if parsing fails
        output_name = sys.argv[4]  # Output file name
    else:
        sys.exit('Wrong number of arguments provided (please provide 4)')  # Exit with an error message if the number of arguments is incorrect

    # Use urllib to fetch HTML content from a YouTube search query
    # After opening the URL, the response from the server is stored in the variable html
    html = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + str(name))
    #This is a regular expression pattern. It looks for strings that match the format "watch?v=" followed by 11 non-whitespace
    #  characters (\S{11}). In YouTube URLs, the video ID is typically 11 characters long.
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())  # Extract video IDs from the HTML content

    # Loop through the specified number of songs
    for i in range(no_of_songs):
        yt = YouTube("https://www.youtube.com/watch?v=" + video_ids[i])  # Create a YouTube object for a video
        print("Downloading File " + str(i + 1) + " .......")  # Print a message to indicate the download progress

        # Download the video in mp3 format (audio only) and save it with a temporary filename
        #filters the available streams for the YouTube video to select only the audio streams.
        mp4files = yt.streams.filter(only_audio=True).first().download(filename='tempaudio-' + str(i) + '.mp3')

    print("Files downloaded.")
    print("Getting the mashup ready.....")

    # Initialize an AudioSegment object with the first audio file and set its duration
    if os.path.isfile("tempaudio-0.mp3"):
        fin_sound = AudioSegment.from_file("tempaudio-0.mp3")[20000:(20+time) * 1000]  # Load the audio and set its duration

    # Loop through the remaining audio files
    for i in range(1, no_of_songs):
        aud_file = str(os.getcwd()) + "/tempaudio-" + str(i) + ".mp3"  # Get the path to the audio file
        #there will be a 1-second crossfade between the end of the 
        # previous audio segment in fin_sound and the beginning of the new segment being appended.
        fin_sound = fin_sound.append(AudioSegment.from_file(aud_file)[10000:(time+10) * 1000], crossfade=0)  # Append the audio to the existing mashup

    try:
        # Export the final mashup as an mp3 file with the specified output name
        fin_sound.export(output_name, format="mp3")
        print("File downloaded successfully. Stored as " + str(output_name))  # Print a success message
    except:
        sys.exit("Error saving file. Try a different file name")  # Exit with an error message if exporting fails

    # Cleanup: Remove the temporary audio files
    if True:  # This condition always evaluates to True and seems unnecessary
        for i in range(no_of_songs):
            os.remove("tempaudio-" + str(i) + ".mp3")

# Entry point of the script
if __name__ == '__main__':
    main()  # Call the main function when the script is executed
    """ 
import threading
from pytube import YouTube
from pydub import AudioSegment
import urllib.request
import re
import os
import sys

def download_video(video_id, output_filename):
    yt = YouTube("https://www.youtube.com/watch?v=" + video_id)
    print("Downloading File " + output_filename + " .......")
    mp4files = yt.streams.filter(only_audio=True).first().download(filename=output_filename)

def main():
    if len(sys.argv) == 5:
        name = sys.argv[1]
        name = name.replace(' ', '') + "songs"
        try:
            no_of_songs = int(sys.argv[2])
            time = int(sys.argv[3])
        except:
            sys.exit("Wrong Parameters entered")
        output_name = sys.argv[4]
    else:
        sys.exit('Wrong number of arguments provided (please provide 4)')

    html = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + str(name))
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    threads = []

    for i in range(no_of_songs):
        video_id = video_ids[i]
        output_filename = 'tempaudio-' + str(i) + '.mp3'

        thread = threading.Thread(target=download_video, args=(video_id, output_filename))
        thread.start()
        threads.append(thread)

        if len(threads) == 4 or i == no_of_songs - 1:
            for thread in threads:
                thread.join()
            threads = []

    print("Files downloaded.")
    print("Getting the mashup ready.....")

    if os.path.isfile("tempaudio-0.mp3"):
        fin_sound = AudioSegment.from_file("tempaudio-0.mp3")[40000:(40+time) * 1000]

    for i in range(1, no_of_songs):
        aud_file = str(os.getcwd()) + "/tempaudio-" + str(i) + ".mp3"
        fin_sound = fin_sound.append(AudioSegment.from_file(aud_file)[20000:(time+20) * 1000], crossfade=0)

    try:
        fin_sound.export(output_name, format="mp3")
        print("File downloaded successfully. Stored as " + str(output_name))
    except:
        sys.exit("Error saving file. Try a different file name")

    if True:
        for i in range(no_of_songs):
            os.remove("tempaudio-" + str(i) + ".mp3")

if __name__ == '__main__':
    main()

