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
nameofprogram = "APTube"
foldername = "DownloadedBy"+nameofprogram
print("===============================******===================================")
print(f"WELCOME TO {nameofprogram}\nTHIS APPLICATION IS MADE BY AKSHAJ")
print("-v1.0")
print("===============================******===================================\n")
print("Procedure:\n  Give the Youtube URL,\n  Check Title and confirm, \n  Select Audio or Video to be downloaded, \n  *For Videos enter 'Tag'(available ahead) for corresponding resolution,\n  *Only highest available bitrate of audio will be downloaded\n  Enjoy offline content!")
print(f"\nAll videos and audios downloaded will be saved in your Videos library in a folder named {foldername}\n")

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
    if os.path.isdir(f'C:\\Users\\{usern}\\Videos\\{foldername}\\') == False:
        os.mkdir(f'C:\\Users\\{usern}\\Videos\\{foldername}\\')
        print("Made Folder for Saving Files..")
    else:
        pass
    return f'C:\\Users\\{usern}\\Videos\\{foldername}\\'

def validate_misc_inputs(prompt,y='y',n='n'):
    while True:
        i = input(prompt)
        if i == y:
            return y
        elif i == n:
            return n
        else:
            print("Invalid input. Try again")

#after download ask for another download
def ask_continuity(): 
    __ = validate_misc_inputs("Do you wish to Download another one? ('y' or 'n') >>")
    if __ == 'y':
        main()
    elif __ == 'n':
        global continue_to_download
        continue_to_download = 0
    
def enter_tag(optionTag):
    print("==================================")
    print("\nEnter the tag of the preffered resolution")
    #To check if input is integer
    while True: 
        try:
            tag = int(input(">>"))
            if tag not in optionTag:
                raise Exception
            else:
                break
        except Exception:
            print('Enter valid Tag (integer)')
    print("==================================")
    return tag

def get_video(video):
    print("Loading download options...")
    f = video.streams.filter(progressive=True)
    optionTag = [stream.itag for stream in f]
    optionQuality = [stream.resolution for stream in f]
    datatoshow = [['Tag', 'Quality']]
    for i in range(len(optionTag)):
        datatoshow.append([optionTag[i], optionQuality[i]])
    choose_tag(video,datatoshow,optionTag)


def checkexistandrename(path,fullfilename):
    tempfilecheckname = os.path.join(path,fullfilename)
    filename,ext = os.path.splitext(fullfilename)
    if os.path.exists(tempfilecheckname):
        i=1
        new_name = f"{filename}({str(i)}){ext}"
        #print(new_name)
        while os.path.exists(os.path.join(path,new_name)) == True: #even new name exists
            i+=1
            new_name = f"{filename}({str(i)}){ext}"
    else:
        new_name = fullfilename
    return new_name

def choose_tag(video,datatoshow,optionTag):
    print(tabulate(datatoshow))
    tag = enter_tag(optionTag)
    print(f"""TO DOWNLOAD:  
        "{video.title}" of :
        Length: {video.length} 
        File Size: {convert_size(int(video.streams.get_by_itag(tag).filesize))}\n
    """)
    confirm = validate_misc_inputs("Do you confirm and acknowledge the size?('y' or 'n')")
    if confirm == 'y':
        print("DOWNLOADING...\nThis program does not show a progress bar. Please wait..")
        try:
            finalvideo = video.streams.get_by_itag(tag)
            path = getdownpath()
            file_present_name = str(video.title) +"." + str(finalvideo.mime_type)[6:]
            new_file_name = checkexistandrename(path,file_present_name)
            #print(file_present_name)          
            finalvideo.download(output_path=path, filename = new_file_name )
            print(f"Your video should have been downloaded. Check the {foldername} folder in Videos library")
        except Exception:
            print("AN ERROR OCCURED!!")
            print("PLEASE CHECK IF YOU HAVE ENTERED CORRECT TAG NUMBER. IF YES, TRY A DIFFERENT TAG")
            print("ALSO, PLEASE CHECK YOUR INTERNET CONNECTION")
        finally:
            ask_continuity()
    #confirm is 'n'        
    else: 
        choose_tag(video,datatoshow,optionTag) ## 


def get_audio(video):
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
    This program does not show a progress bar. Please wait..
    """)
    try:
        finalaudio = video.streams.get_by_itag(optionTag[index])
        path = getdownpath()
        file_present_name = str(video.title) + ".mp3" 
        new_file_name = checkexistandrename(path,file_present_name)
        finalaudio.download(output_path=path,filename = new_file_name)
        #out_file = finalaudio.download(output_path=getdownpath())
        # base, ext = os.path.splitext(out_file)
        # new_file = base + '.mp3'
        # os.rename(out_file, new_file)
        #     
        #     file_present_name = video.title + "." + video.mime_type[6:]
        #     finalvideo.download(output_path=path(),filename = checkexistandrename(path,file_present_name))
        print(f"Your Audio file has been downloaded. Check the {foldername} folder in Videos Library")
        ask_continuity()
    except Exception:
        print("AN ERROR OCCURED")
        print("PLEASE CHECK YOUR INTERNET CONNECTION")
        ask_continuity()

def proceed(video):
    print("==================================")
    print("Do you want AUDIO OR VIDEO (type 'a' or 'v')")
    print("==================================")
    aorv = validate_misc_inputs('>>',y='v',n='a')
    if aorv == 'v':
        get_video(video)       
    elif aorv == 'a':
        get_audio(video)
        

def validate_url():
    validurl=0
    while validurl ==0:
        try:
            url = input("Enter Youtube url here \n>>")
            video = yt(url)
            print("======VIDEO TITLE=================")
            print(video.title)
            print("==================================")
            return video
        except Exception:
            print("Invalid URL. Please Check and try again")
        

def confirm_video(): #just validate_misc_inputs but n refers to main()
    while True:
        _ = input("Do you confirm the video 'y' or else 'n' \n>>")
        if _ == 'y':
            return
        elif _=='n':
            main()
        else:
            print("Invalid input. Try again")

def main():
    while continue_to_download == 1:
        video = validate_url()
        confirm_video()
        proceed(video)
    else:
        global end_called
        if end_called == 1:
            print(f"THANK YOU FOR USING {nameofprogram}. Enjoy your Content!")
            time.sleep(10)
            end_called += 1
        else:
            pass

global end_called   
end_called = 1    

global continue_to_download
continue_to_download = 1  
 
main()

'''
start program
validate url
confirm video
proceed to ask audio or video

validate each small y or n input

once one session is complete ask for another session
    (set by continue to download)
BUGS:
## no backsies once audio is selected
## bug after saying n to confirm in get_video(video) function
'''
'''
getdata(video)
print options
input tag -- vaidate


main
    validateurl
    confirmvideo ##
    proceed
        get video
            choosetag
                ask_continuity


'''