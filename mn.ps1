#!/usr/bin/pwsh

<#
.SYNOPSIS

Quick script to help with rapid journaling.

.EXAMPLE

In PowerShell to start a new note for today:

> vim $(~/src/minion/mn.ps1 -today)

.NOTES

Recommended for your PowerShell profile:

> New-Alias mn ~/src/minion/mn.ps1

.EXAMPLE

> vim $(mn today)


#>
param(
	[switch]$today = $false
)

function JournalToday() {
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
}

if($today){
	JournalToday
}
