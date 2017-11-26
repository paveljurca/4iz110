@echo off
REM Pavel Jurča, xjurp20

:udajeZac
echo %0
echo %date%, %time%
echo .

REM over, ze zadany server existuje
ping -n 1 %1 > debug.txt
IF "%ERRORLEVEL%" EQU "1" goto chyba

REM IF NOT "%DEFINED%" %2 goto chybaPar
set /a "j = %2"

:loop
ping -n 1 -l %j% %1 >> debug.txt
REM zvetsi velikost paketu o 100B
set /a "j = j + 100"
IF "%ERRORLEVEL%" EQU "0" goto loop
IF "%ERRORLEVEL%" EQU "1" goto vysledek

:chyba
echo ZADANY SERVER NEEXISTUJE!
goto end

:chybaPar
echo DRUHY PARAMETR MUSI BYT POCATECNI DELKA PAKETU!
goto end

:vysledek
set /a "j = j - 100"
echo MAXIMALNI DELKA PAKETU PRO %1 je %j%B.

:end
echo .
echo %0
echo %date%, %time%
echo .
