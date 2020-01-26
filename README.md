# Guiparse

给我一个使用了argparse的python脚本，丢给你一个不错的GUI！只需改很少几行贴示例代码段就好！

Give me a python script with argparse, give you back a nice GUI with original function running properly!

![运行截图/Screen Capture](./gui/img/screen_cap.png)

所有的布局、label、按键都会自动根据原argparse的传入参数进行设计和布局。按下Start按键后会把填写好的表单存入`./gui/temp/args.pkl`文件中，并自动开始您原来的`main.py`文件，在main中读取变量值。一切都是自动的。

All of the layout, labels, buttons and bindings will be automatically finished. When you press start button, the input form will be saved into file `./gui/temp/args.pkl`, and automatically start your original main.py file with those values read into main.

# 文件结构/Structure

- `gui.py`: This will be your GUI program entrance. Start your GUI program using `python gui.py`.
- `main.py`: Your original command line main python file. You need to do some arrangement here.
- `guiparse.py`: The guiparse library file. Please don't change its contents unless you are familiar with tkinter and some advanced python skills.

# 使用方法/Usage

## gui.py

```python
from guiparse import *

parser = argStation("Your Project Name Here")

# String
parser.add_argument(
    '--url',
    type=str,
    default="https://mixer.com/browse/games/70323/fortnite",
    help='The url of the starting page.')

parser.add_argument(
    '--root_path',
    type=str,
    is_path=True,
    default="./Data/Mixer_Videos/",
    help='The root path of recorded videos.')
    
# Integer
parser.add_argument(
    '--max_record_num',
    type=int,
    default='5',
    help='The maximum value of records.')
    
# Bool
parser.add_argument(
    '--quality',
    action='store_true',
    help='The quality of recorded videos.')

root = tk.Tk()
#creation of an instance
app = Window(root, parser, main_func="main.py") # Here the 'main.py' is your original main file.
root.geometry(app.geometry)
# start the mainloop 
root.mainloop() 
```

The file template is in the project folder, you can directly copy & paste your parse arguments here and change your main file name properly. All set with it!

## main.py

Just change your main file 
**FROM:**

```python
def main(args):
    pass
if __name__ == "__main__":
    parser = argparse.ArgumentParser('Your Project Name Here')
    parser.add_argument(......)
    args = parser.parse_args()
    main(args)
```
**TO:**

```python
import pickle as pkl
from guiparse import *

def main(args):
    pass

if __name__ == "__main__":
    with open("./gui/temp/args.pkl","rb") as f:
        args=dotdict(pkl.load(f))
    main(args)
```

That's all! Just simply remove the argparse part and replace it by a pickle load. Also remember to import pickle and everything from guiparse. Don't worry about namespace, you can only import some limited names from guiparse! 

**OK, ALL SET!**
Type `python gui.py` to start your gui journey!
