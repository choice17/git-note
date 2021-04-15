## batch file  

### batch command  

* [set variable](#variables)  
* [call program](#call_program)  
* [for loop](#loop)  
* [function](#function)  
* [reference](http://www.trytoprogram.com/batch-file-variables/)  
* [loop for wildcard](#wildcard)  
* [directory loop](#director_wildcard)  

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

### director_wildcard

```batch
echo off
call activate env

call :RUN_CLASSIFICATION

goto :eof

:PROBE
echo PROBE
for /r %%v in ( videos\raw\*_sei.264 ) do (
	echo ffprobe -i %%v
	ffprobe -i %%v 2>> log.txt
)

EXIT /b

:COLLECT
echo COLLECT
for /d %%f in (videos\*) do (
	for /r %%v in ("%%f%"\*_sei.264) do (
		echo cp %%f\%%~nv.264 %%~f_sei.264
		cp %%f\%%~nv.264 %%~f_sei.264
	)
)

EXIT /b

set list=distance multi multi2 multi3 table
for %%s in (%list%) do (
	echo python app.py -app 0 -os 1920 1080 -ofps 12 -noidle -idx -o app-video\%%s-draw.mp4 -u app-video\%%s.mp4
	python app.py -app 0 -os 1920 1080 -ofps 12 -noidle -idx -o app-video\%%s-draw.mp4 -u happ-video\%%s.mp4
)
EXIT /b

:RUN_CLASSIFICATION
echo RUN_CLASSIFICATION
for /d %%f in (videos\*) do (
	for /r %%v in ("%%f%"\*_sei.264) do (
		echo python app.py -app 14 -pwait 9 -os 1920 1080 -ofps 20 -noidle -idx -o output/%%~f_draw.mp4 -u %%f\%%~nv.264
		python app.py -app 14 -pwait 9 -os 1920 1080 -ofps 20 -noidle -idx -o output/%%~f_draw.mp4 -u %%f\%%~nv.264
	)
)
EXIT /b

:RUN_CLASSIFICATION_1DIR
echo RUN_CLASSIFICATION_1DIR
for /r %%f in (videos\raw\*.264) do (
	echo python app.py -app 14 -pwait 9 -os 1920 1080 -ofps 20 -noidle -idx -o output\draw-%%~nf.mp4 -u %%f
	python app.py -app 14 -pwait 9 -os 1920 1080 -ofps 20 -noidle -idx -o output\draw-%%~nf.mp4 -u %%f
)
EXIT /b

:RUN_DRAW_1DIR
echo RUN_CLASSIFICATION_1DIR
for /r %%f in (videos\raw\*.mp4) do (
	echo python app.py -app 0 -os 1920 1080 -ofps 12 -noidle -idx -o videos\draw-%%~nf.mp4 -u %%f
	python app.py -app 0 -os 1920 1080 -ofps 12 -noidle -idx -o videos\draw-%%~nf.mp4 -u %%f
)
EXIT /b


:DUMMY0
set list=166.006.000.luma488_5_0
set list=%list%;166.007.000.multi
set list=%list%;166.008.000.occlusion
set list=%list%;166.009.000.pose
set list=%list%;166.010.000.pose2
EXIT /b

:INSERT_SEI
for /d %%f in (videos\*) do (
	for /r %%v in ("%%f%"\*.mp4) do (
		echo python utils\app.py %%f\%%~nv.264 %%f\%%~nv_sei.264 %%f\%%~nv.ol.csv
		python utils\app.py %%f\%%~nv.264 %%f\%%~nv_sei.264 %%f\%%~nv.ol.csv
	)
)
EXIT /b
```
