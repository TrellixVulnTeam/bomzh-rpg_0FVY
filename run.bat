cd env
cd Scripts
CALL activate.bat
cd ../..

start ngrok.exe http 5000

ping 127.0.0.1 -n 4 > nul

start python D:\program_proj\bomzh-rpg\main.py

ping 127.0.0.1 -n 2 > nul

start python D:\program_proj\bomzh-rpg\updater.py

ping 127.0.0.1 -n 2 > nul

start /D "C:\Users\Dionisiu\AppData\Roaming\Telegram Desktop" telegram.exe --"" tg://resolve?domain=Bomzh_RPG_bot

