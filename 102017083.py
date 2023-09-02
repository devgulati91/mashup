# -*- coding: utf-8 -*-


from pytube import YouTube
from pydub import AudioSegment

import urllib.request
import re
import os
import sys


def main():
    #delete_after_use = True

    if len(sys.argv) == 5:
        name = sys.argv[1]
        name = name.replace(' ','') + "songs"
        try:
            no_of_songs = int(sys.argv[2])
            time = int(sys.argv[3])
        except:
            sys.exit("Wrong Parameters entered")
        output_name = sys.argv[4]
    else:
        sys.exit('Wrong number of arguments provided (pls provide 4)')

    html = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + str(name))
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    for i in range(no_of_songs):
        yt = YouTube("https://www.youtube.com/watch?v=" + video_ids[i]) 
        print("Downloading File "+str(i+1)+" .......")
        mp4files = yt.streams.filter(only_audio=True).first().download(filename='tempaudio-'+str(i)+'.mp3')

    print("Files downloaded.")
    print("Getting the mashup ready.....")

    if os.path.isfile("tempaudio-0.mp3"):
        fin_sound = AudioSegment.from_file("tempaudio-0.mp3")[0:time*1000]
    for i in range(1,no_of_songs):
        aud_file = str(os.getcwd()) + "/tempaudio-"+str(i)+".mp3"
        fin_sound = fin_sound.append(AudioSegment.from_file(aud_file)[0:time*1000],crossfade=1000)
  
    try:
        fin_sound.export(output_name, format="mp3")
        print("File downloaded successfuly. Stored as " + str(output_name))
    except:
        sys.exit("Error saving file. Try differrent file name")
        
    if True:
        for i in range(no_of_songs):
            os.remove("tempaudio-"+str(i)+".mp3")


if __name__ == '__main__':
    main()
