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
	[switch]$tomorrow = $false,
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

function Get-JournalFile() {
	param(
		[DateTime]$date
	)
  $daySlug = '{0:dd}' -f $date
  $ymSlug = '{0:yyyy/MM}' -f $date
	$folder = "~/Journal/$ymSlug"
	$fileName = "$folder/$daySlug.md"

	New-JournalFile -folder $folder -fileName $fileName

	return $fileName

}

<#
.SYNOPSIS

Create journal file and folder path, even if it does not exist.
Add template content if it does not already exist.

#>
function New-JournalFile() {
	param(
	[string]$folder,
	[string]$fileName
	)
	if(-Not(Test-Path -Path $folder)) {
		$_ = New-Item -Type directory -path $folder -Force
	}
	if(-Not(Test-Path -Path $fileName)) {
		$_ = New-Item -Type file -path $fileName -Force
		Add-Content -Path $fileName -Value $today_body
	}
}

<#
.SYNOPSIS

Open journal file for today.

#>
function JournalToday() {
	$date = Get-Date -f 'yyyy-MM-dd'
	$fileName = Get-JournalFile -Date $date
	Write-Output "$fileName"
}

<#
.SYNOPSIS

Open journal file for tomrrow.

#>
function JournalTomorrow() {
	$date = (Get-Date).AddDays(1) -f 'yyyy-MM-dd'
	$fileName = Get-JournalFile -Date $date
	Write-Output "$fileName"
}


if($today){
	JournalToday
}
if($tomorrow){
	JournalTomorrow
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
