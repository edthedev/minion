<#
.SYNOPSIS

Quick commands for Minion use from PowerShell.

.EXAMPLE

In your PowerShell Profile:

```powershell
. C:/src/minion/alias.ps1
```

#>
Write-Host "Adding aliases for Minion..."
if($IsWindows){
	New-Alias mn c:\src\minion\mn.ps1
}else{
	New-Alias mn ~/src/minion/mn.ps1
}

function New-JournalToday() {
	# gvim "$(mn -today)"
	vim "$(mn -today)"
}
New-Alias today New-JournalToday
