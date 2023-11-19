from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
from moviepy.editor import *
from os import walk
from os import listdir
from os.path import isfile, join


def downloadVideo(link, id):
    print(f"Downloading video {id} from: {link}")
    cookies = {
        # Please get this data from the console network activity tool
        # This is explained in the video :)
    }

    headers = {
    'authority': 'ssstik.io',
    'accept': '*/*',
    'accept-language': 'en-US,en;q=0.9,lv;q=0.8,ru;q=0.7',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'hx-current-url': 'https://ssstik.io/ru',
    'hx-request': 'true',
    'hx-target': 'target',
    'hx-trigger': '_gcaptcha_pt',
    'origin': 'https://ssstik.io',
    'referer': 'https://ssstik.io/ru',
    'sec-ch-ua': '"Microsoft Edge";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
    }

    params = {
        'url': 'dl',
    }

    data = {
        'id': link,
        'locale': 'en',
        'tt': 'Vnh4bVdh', # NOTE: This value gets changed, please use the value that you get when you copy the curl command from the network console
    }
    
    print("STEP 4: Getting the download link")
    print("If this step fails, PLEASE read the steps above")
    response = requests.post('https://ssstik.io/abc', params=params, headers=headers, data=data)
    print("Waiting for server to answer...", end="")
    while response.text == "":
        print(".", end="")
        response = requests.post('https://ssstik.io/abc', params=params, headers=headers, data=data)
    print("")

    downloadSoup = BeautifulSoup(response.text, "html.parser")

    downloadLink = downloadSoup.a["href"]
    videoTitle = downloadSoup.p.getText().strip()

    print("STEP 5: Saving the video :)")
    try:
        mp4File = urlopen(downloadLink)
    except:
        print("VIdeo unavailable")
        return

    # Feel free to change the download directory
    with open(f"videos/{id}-video.mp4", "wb") as output:
        while True:
            data = mp4File.read(4096)
            if data:
                output.write(data)
            else:
                break

def parseFile(fileName):
    links = []
    with open(fileName,"r") as outfile:
        data = outfile.readlines()
        for i in data:
            if i != '\n' and len(i) > 5:
                links.append(i[:-1])
    print(links)
    return links

def concatenate(video_clip_paths, output_path, method="compose"):
    """Concatenates several video files into one video file
    and save it to `output_path`. Note that extension (mp4, etc.) must be added to `output_path`
    `method` can be either 'compose' or 'reduce':
        `reduce`: Reduce the quality of the video to the lowest quality on the list of `video_clip_paths`.
        `compose`: type help(concatenate_videoclips) for the info"""
    try:
        # create VideoFileClip object for each video file
        clips = [VideoFileClip(c) for c in video_clip_paths]
        if method == "reduce":
            # calculate minimum width & height across all clips
            min_height = min([c.h for c in clips])
            min_width = min([c.w for c in clips])
            # resize the videos to the minimum
            clips = [c.resize(newsize=(min_width, min_height)) for c in clips]
            # concatenate the final video
            final_clip = concatenate_videoclips(clips)
        elif method == "compose":
            # concatenate the final video with the compose method provided by moviepy
            final_clip = concatenate_videoclips(clips, method="compose")
        # write the output video file
        final_clip.write_videofile(output_path)
    except:
        print("smth went wrong skipping file")
        return

# links = parseFile("links")

# start = 16 # Index from which to start downloading
# i = 0
# for link in links:
#     print(f"downloading {link}")
#     if i >= start:
#         downloadVideo(link, i)
#     i+=1
path = "videos"
onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
print(onlyfiles)
for i in range(len(onlyfiles)):
    onlyfiles[i] = path+"/"+onlyfiles[i]
concatenate(onlyfiles, "final.mp4")