:设定打包文件名称
set srcName=main
set exeName=YoutubeGUI

:执行打包命令
pyinstaller -i youtube.ico -wF %srcName%.py

:复制exe到当前目录
copy .\dist\%srcName%.exe .\%exeName%.exe /Y

:删除过程文件及文件夹
rmdir /s /q __pycache__
rmdir /s /q build
rmdir /s /q dist
del /q %srcName%.spec

.\%exeName%.exe
