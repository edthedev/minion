<#
.SYNOPSIS

Quick commands for Minion use from PowerShell.

.EXAMPLE

In your PowerShell Profile:

```powershell
. C:\src\minion\profiles\alias.ps1
```

#>

function Invoke-JournalToday() {
  vim "$(Get-JournalToday)"
}

function Invoke-JournalTomorrow() {
  vim "$(Get-JournalTomorrow)"
}

function Invoke-JournalYesterday() {
  vim "$(Get-JournalYesterday)"
}

function New-JournalNote() {
	param(
		[string]$title
	)
  vim "$(Get-JournalNote $title)"
}

function Open-JournalNote() {
	param(
		[string]$tag
	)
	$fileName = "$(minion.exe -search $tag)"
	vim $fileName
}

New-Alias today Invoke-JournalToday
New-Alias tomorrow Invoke-JournalTomorrow
New-Alias yesterday Invoke-JournalYesterday
New-Alias note New-JournalNote
