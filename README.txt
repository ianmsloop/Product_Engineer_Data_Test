Product Engineer Data Test
Author: Ian Sloop
Email: ianmsloop@gmail.com, Please contact me with questions
Date: 10/27/2020

Use Python 3.7.9 as your project interpreter, as it is a stable release.
Download: https://www.python.org/downloads/release/python-379/

PyCharm Community Edition is a recommended IDE
Download: https://www.jetbrains.com/pycharm/download/#section=windows

Installing Project Requirements:
Install the requirements located in Scripts\requirements.txt by opening CMD as an administrator
(right click for this option on the icon) and navigating to your python directory (e.x.= cd C:\Python37).
Navigate one directory deeper with "cd Scripts" (omitting the " "), then type "where pip".
The result should be your current directory. Install the python requirements with
"pip install -r C:\Users\ianms\Desktop\Product_Engineer_Data_Test\requirements.txt" except in your case
use the full path of your project, not the placeholder here. If the command executes successfully,
you can view your installed packages with "pip list".

Running Scripts:
It is recommended to use a Python IDE for the best experience running scripts. I recommend PyCharm
Community edition as it is free, has high functionality, and is easy to use. Once you have downloaded
a Python IDE and know what you are doing, you can run Scripts\charge_power_availibilty.py and it will display and 
save plots of the data analysis results to Plots\. If you are unfamiliar with Python, it is important that your
project uses the correct version of Python with the correct associated packages, or else the scripts
will not function. If you have only one installed version of Python, your IDE should recognize it automatically,
but if there are issues the project interpreter can be set manually. In PyCharm, go to File\Settings
and click on the cog in the top right and click add. You will then check "Existing Environment",
click on the "..." and navigate to python.exe (e.x.= C:\Python37\python.exe). Once this is set, make
sure that you have selected this new environment in the top taskbar under "Edit Configurations", just to
the left of the green arrow. Once this is done run python with the green arrow in the top right hand corner.