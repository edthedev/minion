#!/usr/bin/pwsh

<#
.SYNOPSIS

Quick functions to help with rapid journaling.

.EXAMPLE

In PowerShell to start a new note for today:

> vim $(Get-JournalToday)

.EXAMPLE

In PowerShell to start a new note with a title:

> vim $(Get-JournalNote -Title "This is my title")

.EXAMPLE

In PowerShell to start a new note for tomorrow:

> vim $(Get-JournalTommorow)

.NOTES

Recommended for your PowerShell profile:

> $env:minion = "c:\src\minion"
> Import-Module $env:minion\modules\minion.psm1
> function Invoke-JournalToday {
>     vim $(Get-JournalToday)
> }
> New-Alias today Invoke-JournalToday

See profile/alias.ps1 for more examples.

#>
param(
	[switch]$today = $false,
	[switch]$tomorrow = $false,
	[string]$title
)


function Get-JournalTemplate() {
	param(
		[string]$date
	)
	$prettyDate = '{0:yyyy MMMM dd}' -f $date
	$prettyDate = Get-Date -Format "yyyy MMMM dd"
	# $template = Get-Content -Path $env:minion\templates\journal_template.txt
	$template = @"
Journal {0}

# {0} Plan"

## Self Care

## Strategic Investment

## Operational Commitment

## Fun
"@
	$body = $template -f $prettyDate, $prettyDate
	return $body
}

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
	[string]$fileName,
	[DateTime]$date
	)
	if(-Not(Test-Path -Path $folder)) {
		$_ = New-Item -Type directory -path $folder -Force
	}
	if(-Not(Test-Path -Path $fileName)) {
		$_ = New-Item -Type file -path $fileName -Force
		$today_body = Get-JournalTemplate -Date $date
		# Add-Content -Path $fileName -Value $today_body
		Set-Content -Path $fileName -Value $today_body
	}
}

<#
.SYNOPSIS

Open journal file for today.

#>
function Get-JournalToday() {
	$date = Get-Date -f 'yyyy-MM-dd'
	$fileName = Get-JournalFile -Date $date
	return "$fileName"
}

<#
.SYNOPSIS

Open journal file for tomrrow.

#>
function Get-JournalTomorrow() {
	$date = (Get-Date).AddDays(1) -f 'yyyy-MM-dd'
	$fileName = Get-JournalFile -Date $date
	return "$fileName"
}

<#
.SYNOPSIS

Open journal file for yesterday.

#>
function Get-JournalYesterday() {
	$date = (Get-Date).AddDays(-1) -f 'yyyy-MM-dd'
	$fileName = Get-JournalFile -Date $date
	return "$fileName"
}

<#
.SYNOPSIS

Open journal file for the given title.
Store it in a folder named for this month.

#>
function Get-JournalNote() {
	param(
	[string]$title
	)
	$ymSlug = Get-Date -Format "yyyy/MM"
	$folder = "~/Journal/$ymSlug"
	if(-Not(Test-Path -Path $folder)) {
		$_ = New-Item -Type directory -path $folder -Force
	}
	$titleSlug = $title.replace(' ','_')
	$fileName = "$folder/$titleSlug.md"
	return "$fileName"

}


Export-ModuleMember -Function Get-JournalFile
Export-ModuleMember -Function Get-JournalToday
Export-ModuleMember -Function Get-JournalTomorrow
Export-ModuleMember -Function Get-JournalYesterday
Export-ModuleMember -Function Get-JournalNote


