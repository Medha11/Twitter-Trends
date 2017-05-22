@echo off
for %%A in ("%~dp0.") do set parent=%%~dpA
for %%A in ("%parent%.") do set parent=%%~dpA



C:\windows\system32\msiexec /qn+ /i "%parent%miscellaneous\dependencies\mongodb-win32-x86_64-2008plus-ssl-3.0.7-signed.msi" ^
            INSTALLLOCATION="%parent%engine\MongoDB" ^
            ADDLOCAL="all"

mkdir "%parent%engine\MongoDB\db"
