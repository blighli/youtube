:设定打包文件名称
set name=main

:执行打包命令
pyinstaller -i youtube.ico -wF %name%.py

:复制exe到当前目录
copy .\dist\%name%.exe .

:删除过程文件及文件夹
rmdir /s /q __pycache__
rmdir /s /q build
rmdir /s /q dist
del /q %name%.spec
