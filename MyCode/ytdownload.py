from pytube import YouTube as yt
import os
import math
import time
from tabulate import tabulate
print("""\n\n
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@%##########################%@@@@@@@@@@@@
@@@@@@@@%###########+*.###############@@@@@@@@@@@
@@@@@@@@############     +*###########@@@@@@@@@@@
@@@@@@@@############   .+#############@@@@@@@@@@@
@@@@@@@@%###########+*################@@@@@@@@@@@
@@@@@@@@@%##########################%@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
""")

print("===============================******===================================")
print("WELCOME TO YOUTUBE DOWNLOADER\nTHIS APPLICATION IS MADE BY AKSHAJ")
print("-v0.3")
print("===============================******===================================\n")
print("Process:\n  Give the Youtube URL,\n  Check Title and confirm, \n  Select Audio or Video to be downloaded, \n  *For Videos enter Tag for corresponding resolution,\n  *Only highest available bitrate of audio will be downloaded\n  Enjoy offline content!")
print("All videos and audios downloaded will be saved in your Videos library in a folder named DownloadedByPyTube\n")
def convert_size(size_bytes):
   if size_bytes == 0:
       return "0B"
   size_name = ("B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB")
   i = int(math.floor(math.log(size_bytes, 1024)))
   p = math.pow(1024, i)
   s = round(size_bytes / p, 2)
   return "%s %s" % (s, size_name[i])

def getdownpath():
    usern = os.environ['USERNAME']
    if os.path.isdir(f'C:\\Users\\{usern}\\Videos\\DownloadedByPyTube\\') == False:
        os.mkdir(f'C:\\Users\\{usern}\\Videos\\DownloadedByPyTube\\')
        print("Made Folder for Saving Files..")
    else:
        pass
    return f'C:\\Users\\{usern}\\Videos\\DownloadedByPyTube\\'


url = input("Enter Youtube url here >>")
video = yt(url)
print("======VIDEO TITLE=================")
print(video.title)
print("==================================")
proceed = input("If you wish to proceed say 'y' or else 'n' \n>>")
if proceed == 'y':
    print("==================================")
    print("Do you want AUDIO OR VIDEO (type 'a' or 'v')")
    print("==================================")
    aorv = input('>>')
    if aorv == 'v':
        print("Loading download options...This may take time...")
        f = video.streams.filter(progressive=True)
        optionTag = [stream.itag for stream in f]
        optionQuality = [stream.resolution for stream in f]
        datatoshow = [['Tag', 'Quality','Size']]
        for i in range(len(optionTag)):
            datatoshow.append([optionTag[i], optionQuality[i],convert_size(int(video.streams.get_by_itag(optionTag[i]).filesize))])
        print(tabulate(datatoshow))
        print("==================================")
        print("\nEnter the tag of the preffered resolution")
        tag = int(input(">>"))
        print("==================================")
        print(f"""DOWNLOADING...  
    "{video.title}" of :
    Length: {video.length} 
    File Size: {convert_size(int(video.streams.get_by_itag(tag).filesize))}\n
    Press Ctrl+C or close the window to stop the program
    This program does not show a progress bar. Please wait..
        """)

        try:
            finalvideo = video.streams.get_by_itag(tag)
            finalvideo.download(output_path=getdownpath())
            print("Your video should have been downloaded. Check the DonwloadedByPytube folder in Videos library")
            print("This window will close in 10 seconds")
            time.sleep(10)
        except Exception:
            print("AN ERROR OCCURED!!")
            print("PLEASE CHECK IF YOU HAVE ENTERED CORRECT TAG NUMBER. IF YES, TRY A DIFFERENT TAG")
            print("ALSO, PLEASE CHECK YOUR INTERNET CONNECTION")
            print("This window will close in 10 seconds")
            time.sleep(10)

    elif aorv == 'a':
        f = video.streams.filter(mime_type='audio/mp4')
        optionQuality = [int(stream.abr[:-4]) for stream in f]
        optionTag = [stream.itag for stream in f]
        index = 0
        m = max(optionQuality)
        for i in range(len(optionQuality)):
            if optionQuality[i]==m:
                break
            else:
                index+=1
        print(f"""DOWNLOADING...  
    "{video.title}" of :
    Length: {video.length} 
    File Size: {convert_size(int(video.streams.get_by_itag(optionTag[index]).filesize))}\n
    Press Ctrl+C or close the window to stop the program
    This program does not show a progress bar. Please wait..
        """)

        try:
            finalaudio = video.streams.get_by_itag(optionTag[index])
            out_file = finalaudio.download(output_path=getdownpath())
            base, ext = os.path.splitext(out_file)
            new_file = base + '.mp3'
            os.rename(out_file, new_file)
            print("Your Audio file has been downloaded. Check the DownloadedByPyTube folder in Videos Library")
            print("This window will close in 10 seconds")
            time.sleep(10)
        except Exception:
            print("AN ERROR OCCURED")
            print("PLEASE CHECK YOUR INTERNET CONNECTION")
            print("This window will close in 10 seconds")
            time.sleep(10)

else:
    print('Exited out of program')
    
