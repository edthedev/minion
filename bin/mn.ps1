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
	[switch]$today = $false,
	[string]$title
)

$prettyDate = Get-Date -Format "yyyy MMMM dd"
$today_template = @'
# {0} Journal"

## Self Care

## Investment

## Fun
'@
$today_body = $today_template -f $prettyDate

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
		Add-Content -Path $fileName -Value $today_body
	}
	Write-Output "$fileName"
}

if($today){
	JournalToday
}

if($title){
	$ymSlug = Get-Date -Format "yyyy/MM/dd"
	$folder = "~/Journal/$ymSlug"
	if(-Not(Test-Path -Path $folder)) {
		$_ = New-Item -Type directory -path $folder -Force
	}
	$titleSlug = $title.replace(' ','_')
	$fileName = "$folder/$titleSlug.md"
	Write-Output "$fileName"
}
