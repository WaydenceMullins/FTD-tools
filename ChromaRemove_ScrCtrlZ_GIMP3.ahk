;1. Open GIMP 3 and create new image, usually 900x900, making sure that "Fill with" in "Advanced options" is set to "Transparency"
;2. Drag and drop the images into layers (bottom right)
;3. Delete the Background layer, make sure that "Merge filter" is checked (can be found in Colors > Hue-Saturation)
;4. Hit Alt+Z, enter the number of images to edit, hit Enter twice
;5. When it's done, a window prompting to export it will pop up. Choose a location and click Export.
;6. Open the exported file as an archive (rename to .zip or use 7-Zip). The images can be found in data folder.

#NoEnv  ; Recommended for performance and compatibility with future AutoHotkey releases.
; #Warn  ; Enable warnings to assist with detecting common errors.
SendMode Input  ; Recommended for new scripts due to its superior speed and reliability.
SetWorkingDir %A_ScriptDir%  ; Ensures a consistent starting directory.

CoordMode Mouse, Screen		;swith to screen coords
targetColorX := 660			;horizontal coords to pick target color from
targetColorY := 270			;vertical

sleepTimerShort := 200		;time between operations
sleepTimerMedium := 600		;adjust these if your PC can't keep up
sleepTimerLong := 7000		;this is 7 seconds

!z::																									;on Alt+Z
{InputBox, ImageCount, Remove Chromakey, Number of images to process`nHold Home to stop, , 210, 180, , , , , 1													;window asking for picture count, default 1
if ErrorLevel
    Return																											;if cancel, reset
InputBox, ScaleImageTo, Remove Chromakey,After that Scale Image...`nThen open Export As...`nAnd select OpenRaster (.ora)`n0 to skip, , 210, 180, , , , , 300	;window asking for scale image, default 300
if ErrorLevel
    Return																											;if cancel, reset
else {
		ImagesProcessed := 0
		while ImageCount > ImagesProcessed
		{
			Sleep, sleepTimerShort
			Send +o											;switch to select by color tool
			Sleep, sleepTimerShort
			Send {Click, %targetColorX% %targetColorY%}		;click on target color
			Sleep, sleepTimerShort
			Send {F10}
			Send s
			Send g
			Send {Enter}									;select grow selection
			Sleep, sleepTimerShort
			Send 2											;enter number
			Send {Tab 3}
			Send {Enter}									;apply grow selection
			Sleep, sleepTimerShort
			if (GetKeyState("Home"))						;hold Home to stop
				Break
			Send {F10}
			Send c
			Send a
			Send a
			Send {Enter}									;select color to alpha
			Sleep, sleepTimerShort
			Send {Tab 3}
			Send {Enter}									;select target color picker
			Sleep, sleepTimerShort
			Send {Click, %targetColorX% %targetColorY%}		;click on target color
			Sleep, sleepTimerShort
			Send {Tab}										;window unfocused, tab to hide window
			Sleep, sleepTimerShort
			Send {Tab}										;tab again to focus on window
			if (GetKeyState("Home"))						;hold Home to stop
				Break
			Sleep, sleepTimerShort
			Send {Tab 6}
			Send 0.01										;select opacity threshold slider and enter number
			Send {Tab 11}
			Send {Enter}									;apply color to alpha
			Sleep, sleepTimerMedium
			Send {F10}
			Send c
			Send {Down 3}
			Send {Enter}									;select hue-saturation
			Sleep, sleepTimerShort
			Send !{m 2}										;highlight magenta (Alt+M)									
			Send {Space}									;select it (Alt+M)
			Send {Tab 5}
			Send -100										;select saturation slider and enter number
			Send {Tab 11}
			Send {Enter}									;apply hue-saturation
			Sleep, sleepTimerMedium
			Send {PgDn}										;next layer
			ImagesProcessed++
			if (GetKeyState("Home"))						;hold Home to stop
				Break
		}
		if (ScaleImageTo > 0 and (GetKeyState("Home")) != True)
		{
			Sleep, sleepTimerShort
			Send {F10}
			Send i
			Send s
			Send {Enter}									;open Scale Image...
			Sleep, sleepTimerShort
			Send {Tab}
			Sleep, sleepTimerShort
			Send %ScaleImageTo%								;enter scaling value
			Sleep, sleepTimerShort
			Send {Tab 2}
			Send %ScaleImageTo%								;2nd time
			Send {Tab}
			Send {Home}										;make sure we're scaling in pixels
			Sleep, sleepTimerShort
			Send {Tab 5}
			Send {Home}
			Send {Down 2}									;make sure we're in the right scaling mode
			Send {Tab 3}
			Send {Enter}									;apply scaling
			Sleep, sleepTimerLong
			Send {F10}
			Send f
			Send x
			Send x
			Send {Enter}									;open Export As
			Sleep, sleepTimerShort
			Send +{Tab 5}									;go to Select File Type
			Sleep, sleepTimerShort
			Send {Space}
			Sleep, sleepTimerShort
			Send {Down 31}									;go to OpenRaster
		}
	}
}
Return
^k::																											;on Ctrl+K
{InputBox, ScreenshotCount, Screenshot Ctrl+Z, Number of screenshots to take`nHold Esc to stop, , 210, 140		;create window asking for screenshot count
if ErrorLevel
    Return																										;if cancel, reset
else {
		ScreenshotsTaken := 0
		while ScreenshotCount > ScreenshotsTaken
		{
			Sleep, 300
			Send ^{Backspace}				;Ctrl+Bacspace
			Sleep, 300
			Send b
			Sleep, 300
			Send ^z
			Sleep, 300
			Send b
			ScreenshotsTaken++
			if (GetKeyState("Home"))		;hold Home to stop
				Break
		}
	}
}
Return