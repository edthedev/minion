<#
.SYNOPSIS

Quick commands for Minion use from PowerShell.

.EXAMPLE

In your PowerShell Profile:

```powershell
. C:\src\minion\profiles\alias.ps1
```

#>
Write-Host "Adding aliases for Minion..."

if(! $IsWindows) {
	# Bootstrap for older PowerShell
	$IsWindows = ($env:OS -eq "Windows_NT")
}

# if($IsWindows){
	# New-Alias mn c:\src\minion\bin\mn.ps1
# }else{
	# Write-Host "??? $IsWindows ???"
	# New-Alias mn ~/src/minion/bin/mn.ps1
# }

## TODO: Clean this up by converting the script into a module.
function Invoke-JournalToday() {
  vim "$(Get-JournalToday)"
}

function Invoke-JournalTomorrow() {
  vim "$(Get-JournalTomorrow)"
}

function New-JournalNote($title) {
  vim "$(Get-JournalNote $title)"
}

New-Alias today Invoke-JournalToday
New-Alias tomorrow Invoke-JournalTomorrow
New-Alias note New-JournalNote
