REM ## 打包tarndo服务程序，生成main.exe
REM ## main.exe 重命名为service.exe

REM ## 打包electron, 生成window平台exe文件，包含ia32和x64平台，入口执行文件为tmxtools.exe

REM ## 移动service.exe，dtd等文件到electron app的根目录


buildtornado.bat

node --harmony build.js

REM xcopy 

