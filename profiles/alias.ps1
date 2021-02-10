<#
.SYNOPSIS

Quick commands for Minion use from PowerShell.

.EXAMPLE

In your PowerShell Profile:

```powershell
. C:\src\minion\profiles\alias.ps1
```

#>
Write-Host "+ Added aliases for Minion..."

if(! $IsWindows) {
	# Bootstrap for older PowerShell
	$IsWindows = ($env:OS -eq "Windows_NT")
}

if($IsWindows){
	New-Alias mn c:\src\minion\bin\mn.ps1
}else{
	New-Alias mn ~/src/minion/bin/mn.ps1
}

function New-JournalToday() {
	# gvim "$(mn -today)"
	vim "$(mn -today)"
}

function New-JournalNote($title) {
	vim "$(mn -Title $title)"
}

New-Alias today New-JournalToday
New-Alias note New-JournalNote
