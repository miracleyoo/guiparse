# Usage: Download live stream in Mixer under one topic in batch.
#        You can also adapt it easily to other live stream site
#        with some basic knowledge in `selenium`.
#        When a stream is finished, auto check and correction for
#        recorded video will be performed, and the corrected video
#        file will be saved in $root_path/processed.
#        Some examples of the starting url:
#        https://mixer.com/
#        https://mixer.com/browse/games/70323/fortnite
#        https://mixer.com/browse/games/14580/overwatch
# Author: Zhongyang Zhang
# E-mail: mirakuruyoo@gmail.com

from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

import argparse
import multiprocessing
import os
import time
import subprocess
import datetime
import signal
import sys
import pickle as pkl
from pathlib2 import Path
from guiparse import *


REFRESH_TIME = 15
TIMEOUT_FIRST = 5
TIMEOUT_SCROLL = 3

# Timing for a code block using "with"
class Timer(object):
    def __init__(self, name=None):
        self.name = name

    def __enter__(self):
        self.t_start = time.time()

    def __exit__(self, type, value, traceback):
        print("==> [%s]:\t" % self.name, end="")
        self.time_elapsed = time.time() - self.t_start
        print("Elapsed Time: %s (s)" % self.time_elapsed)

# Print with nice format and exect time stamp
def log(*snippets, end=None):
    if end is None:
        print(time.strftime("==> [%Y-%m-%d %H:%M:%S]", time.localtime()
                            ) + " " + "".join([str(s) for s in snippets]))
    else:
        print(time.strftime("==> [%Y-%m-%d %H:%M:%S]", time.localtime()) + " " + "".join([str(s) for s in snippets]),
              end=end)

# Correct all of the rest videos currently in the "raw" folder
def correct_rest_videos():
    video_paths = [i for i in list(
        (args.root_path/"raw").iterdir()) if i.is_file() and not i.name.startswith(".")]
    for video_path in video_paths:
        check_video(video_path)

# Check and correct a video in the certain path. 
def check_video(video_path):
    video_path = Path(video_path)
    processed_video_path = Path(
        *video_path.parts[:-2], "processed", video_path.name)
    if(os.path.exists(video_path) is True):
        try:
            with Timer(video_path.name+" check"):
                subprocess.call(["ffmpeg", '-err_detect', 'ignore_err', '-i', video_path,
                                 '-c', 'copy', processed_video_path])
                os.remove(str(video_path))
        except Exception as e:
            log(e)
    else:
        log("Skip fixing. File not found.")
    log("Fixing of video " + video_path.name +
        " is done. Going back to checking..")

# Start a recorder process for a certain streamer. After recording, check and correct it.
def mixer_recorder(streamer_name):
    # start streamlink process
    log("Start recording for ", streamer_name)
    recorded_filename = args.root_path/"raw" / \
        (streamer_name+"_"+datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")+".mp4")
    with Timer(recorded_filename.name+" download"):
        subprocess.run(["streamlink", "https://mixer.com/" +
                        streamer_name, args.quality, "-o", recorded_filename])

    log("Recording stream " + recorded_filename.name +
        " is done. Fixing video file.")
    check_video(recorded_filename)
    return args.root_path/"processed"/recorded_filename.name

# Use selenium to dynamically analyze the input url page and get the list
# of streamer name in this page.
def analyze_mixer_page(url):
    driver = webdriver.Chrome()
    driver.get(url)
    element_present = EC.presence_of_element_located(
        (By.TAG_NAME, 'b-simple-browse-card'))
    WebDriverWait(driver, TIMEOUT_FIRST).until(element_present)
    for i in range(args.scroll_page_num):
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(TIMEOUT_SCROLL)
    time.sleep(TIMEOUT_FIRST)
    elems = driver.find_elements_by_tag_name("b-simple-browse-card")
    streamer_names = [i.find_element_by_tag_name(
        "a").get_attribute("href").split("/")[-1] for i in elems]
    driver.close()
    log(str(len(streamer_names))," names extracted!")
    return streamer_names

# Actions when detect a exit signal like `Ctrl+C`
def signal_handler(sig, frame):
    p.terminate()
    p.join()
    correct_rest_videos()
    log('Program exit successfully and video recorded corrected!\nThank for using!')
    sys.exit(0)

def parse_url(url,args):
    signal.signal(signal.SIGINT, signal_handler)
    correct_rest_videos()
    streamer_names = analyze_mixer_page(url)
    result = p.map(mixer_recorder, streamer_names[:args.max_record_num])
    log(str(len(result)), "Videos has been successfully recorded! Thanks for using.")

def main(args):
    args.root_path = Path(args.root_path)/args.class_name

    if not args.root_path.exists():
        os.makedirs(str(args.root_path))
    if not (args.root_path/"raw").exists():
        os.makedirs(str((args.root_path/"raw")))
    if not (args.root_path/"processed").exists():
        os.makedirs(str((args.root_path/"processed")))

    parse_url(args.url,args)

if __name__ == "__main__":
    with open("./gui/temp/args.pkl","rb") as f:
        args=dotdict(pkl.load(f))
    p = multiprocessing.Pool(processes=args.max_record_num)
    main(args)


