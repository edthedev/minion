<#
.SYNOPSIS

Quick commands for Minion use from PowerShell.

.EXAMPLE

In your PowerShell Profile:

```powershell
. C:\src\minion\profiles\alias.ps1
```

#>
$editor = "vim"

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


<#
function Open-JournalNotes() {
	param(
		[string]$tag
	)
	$fileNames = "$(minion.exe -search $tag)"
	vim $fileNames
}
#>

# Quick notes with vim.
New-Alias today Invoke-JournalToday
New-Alias tomorrow Invoke-JournalTomorrow
New-Alias yesterday Invoke-JournalYesterday
New-Alias note New-JournalNote
New-Alias todo Get-JournalTodos

# Commands for within Vim
function Find-JournalNotes() {
	param(
		[string]$tag
	)
	$fileNames = "$(minion.exe -search $tag)"
	return $fileNames
}

