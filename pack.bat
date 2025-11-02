:设置exe文件名称
set name=YoutubeGUI

:执行打包命令生成exe文件
pyinstaller --add-binary "assets;assets" -i "assets\youtube.ico" -wF main.py -n %name%

:运行生成的exe程序
dist\%name%.exe
