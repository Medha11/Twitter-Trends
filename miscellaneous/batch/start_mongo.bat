@echo off

for %%A in ("%~dp0.") do set parent=%%~dpA
for %%A in ("%parent%.") do set parent=%%~dpA

CALL "%parent%engine\MongoDB\bin\mongod.exe" --dbpath "%parent%engine\MongoDB\db"
