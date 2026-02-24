@echo off
chcp 65001 >nul
title i-cup 远程安装程序启动器
color 0A

echo.
echo ==============================
echo      i-cup 安装程序助手
echo ==============================
echo 正在从服务器下载安装程序...
echo （请稍等，速度取决于你的网络）
echo.

:: 关键：替换为你的蓝奏云/百度网盘直链
set "PAN_URL=@echo off
chcp 65001 >nul
title i-cup 远程安装程序启动器
color 0A

echo.
echo ==============================
echo      i-cup 安装程序助手
echo ==============================
echo 正在从服务器下载安装程序...
echo （请稍等，速度取决于你的网络）
echo.

:: 关键：替换为github连接
set "PAN_URL=https://github.com/conrad-2026/i-cup/releases/download/v1.0/xbonekey.exe"
set "EXE_NAME=xbonekey.exe"

:: 自动打开网盘下载页面（用户只需点击“普通下载”即可）
start "" "%PAN_URL%"

echo.
echo ==============================
echo 已为你打开下载页面，请：
echo 1. 点击页面中的「普通下载」按钮
echo 2. 下载完成后，双击下载的%EXE_NAME%运行
echo ==============================

:: 停留20秒，让用户看清提示
timeout /t 20 /nobreak >nul
exit"
set "EXE_NAME=xbonekey.exe"

:: 自动打开网盘下载页面（用户只需点击“普通下载”即可）
start "" "%PAN_URL%"

echo.
echo ==============================
echo 已为你打开下载页面，请：
echo 1. 点击页面中的「普通下载」按钮
echo 2. 下载完成后，双击下载的%EXE_NAME%运行
echo ==============================

:: 停留20秒，让用户看清提示
timeout /t 20 /nobreak >nul
exit