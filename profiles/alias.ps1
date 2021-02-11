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

function New-JournalNote($title) {
  vim "$(Get-JournalNote $title)"
}

New-Alias today Invoke-JournalToday
New-Alias tomorrow Invoke-JournalTomorrow
New-Alias yesterday Invoke-JournalYesterday
New-Alias note New-JournalNote
