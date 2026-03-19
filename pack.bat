:设置exe文件名称
set name=YoutubeGUI

:获取git版本号
python get_version.py

:执行打包命令生成exe文件
uv run pyinstaller --add-binary "assets;assets" -i "assets\youtube.ico" -wF main.py -n %name% --clean

:运行生成的exe程序
dist\%name%.exe
