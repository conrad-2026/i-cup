@echo off
chcp 65001 >nul
echo ==============================
echo i-cup 安装程序启动中...
echo ==============================
:: 替换为你的主程序exe路径（若和脚本同目录，直接写exe文件名即可）
start "" "xbonekey.exe"
:: 启动后停留5秒，让用户看到提示
timeout /t 5 /nobreak >nul
exit