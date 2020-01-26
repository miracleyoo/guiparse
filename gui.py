from guiparse import *

parser = argStation("Mixer Video Downloader")

# String
parser.add_argument(
    '--url',
    type=str,
    default="https://mixer.com/browse/games/70323/fortnite",
    help='The url of the starting page.')

parser.add_argument(
    '--root_path',
    type=str,
    default="./Data/Mixer_Videos/",
    help='The root path of recorded videos.')

parser.add_argument(
    '--class_name',
    type=str,
    default="default",
    help='The genre or type of stream videos in this input url.')

parser.add_argument(
    '--quality',
    type=str,
    default="best",
    help='The quality of recorded videos.')

# Integer
parser.add_argument(
    '--max_record_num',
    type=int,
    default='5',
    help='The maximum value of records.')

parser.add_argument(
    '--scroll_page_num',
    type=int,
    default='2',
    help='The number of pages you scrolls down.')

root = tk.Tk()
#creation of an instance
app = Window(root, parser, main_func="main.py")
root.geometry(app.geometry)
#mainloop 
root.mainloop() 