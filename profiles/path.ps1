# Example Usage in PowerShell Profile
# $env:src = "c:\src"
# $env:minion = "$env:src\minion
# . $env:minion\profiles\path.ps1

$ENV:PATH+=";c:\src\minion\go" 
$ENV:PATH+=";c:\src\minion\go\chart" 
$ENV:PATH+=";c:\src\minion\go\agenda" 
Write-Host "+ Added minion command to path."
