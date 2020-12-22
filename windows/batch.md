## batch file  

### batch command  

* [set variable](#variables)  
* [call program](#call_program)  
* [for loop](#loop)  
* [function](#function)  
* [reference](http://www.trytoprogram.com/batch-file-variables/)  
* [loop for wildcard](#wildcard)  

### variables  

```
:: array (string)
set files= a.exe b.md c.png

:: for assigning numeric value
set /A variable_name=nameric_value
```

### call_program    

```
call activate venv
call python app.py
```

### loop

```
:: https://stackoverflow.com/questions/7522740/counting-in-a-for-loop-using-windows-batch-script (return global for local scope)

setlocal
set /a count = 1
:: (start,step,end)
for /L %a in (1,5,100) do (
	set /a count += 1
	echo !count!
	echo %a
)
endlocal && set count=%count%
```

```batch
REM run for loop in bat script
:: for loop in function and return val

call :FORR 20,ret
echo %ret%
pause

:FORR
set /A count = 0
setlocal
(for /L %%a in (0,%1%,100) do (
	set /a count += 1
	echo %%a
))
endlocal && set %~2=%count%
EXIT /B 0
```

### function    

```batch
echo off
set files= a.exe b.md c.png
call activate venv
pyinstaller prog.spec
call :INFO Make dir to "%1"
mkdir "releasepath\%1\"
(for %%a in (%files%) do (
	call :COPYING %%a releasepath\%1\
))
call :INFO DONE.
call deactivate
:END
echo bye ...
pause

:COPYING
call :INFO Copying %1
copy %1 %2
EXIT /B 0

:INFO
echo [INFO] %*
EXIT /B 0
```

### wildcard  

```batch
for /r %%v in (*.264) do ffmpeg -i %%~nxv -c copy %%~nv.mp4
```
