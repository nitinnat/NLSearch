Dim oShell
Set oShell = WScript.CreateObject ("WScript.Shell")
oShell.run "C:\Python27\Scripts\jupyter notebook", 0
Set oShell = Nothing