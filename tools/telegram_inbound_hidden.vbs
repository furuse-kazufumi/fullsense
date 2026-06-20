' Hidden launcher for FullSense Telegram inbound — runs the original cmd line with a HIDDEN window
' so the 10-min scheduled task no longer flashes a console (the "チラチラ" fix, 2026-06-20).
' Window style 0 = hidden, wait=False. Reversible: point the task action back to:
'   cmd.exe  /c "py -3.11 D:\projects\fullsense\tools\fullsense_telegram_inbound.py >> D:\backup\logs\fullsense_telegram_inbound.log 2>&1"
CreateObject("WScript.Shell").Run "cmd /c ""py -3.11 D:\projects\fullsense\tools\fullsense_telegram_inbound.py >> D:\backup\logs\fullsense_telegram_inbound.log 2>&1""", 0, False
