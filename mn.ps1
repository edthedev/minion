#!/usr/bin/pwsh

<#
.EXAMPLE

In PowerShell to start a new note for today:

> vim $(~/src/minion/mn.ps1)

#>

$daySlug = Get-Date -Format "dd"
$ymSlug = Get-Date -Format "yyyy/MM"
$folder = "~/Journal/$ymSlug"
$fileName = "$folder/$daySlug.md"

if(-Not(Test-Path -Path $folder)) {
	$_ = New-Item -Type directory -path $folder -Force
}
if(-Not(Test-Path -Path $fileName)) {
	$_ = New-Item -Type file -path $fileName -Force
}
Write-Output "$fileName"
