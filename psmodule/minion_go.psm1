#!/usr/bin/pwsh

<#
.SYNOPSIS

Functions that rely on the compiled Minion Go executable.
This tool is for quick text searching across Journal notes.

.EXAMPLE

List Todo (+ [] foo) lines in Journal files.

> Get-JournalTodos -Max 10
>
.EXAMPLE

Get a quick count of todo (+ [ ] foo) lines in Journal files.

> Get-JournalTodos -Max 10

#>

function Get-JournalTodos() {
	param(
		[switch]$all = $false,
		[int]$maximum = 20
	)
	if($all) {
		minion.exe -todo
	} else {
		minion.exe -todo | Select-Object -Last $maximum
	}
}

<#
.SYNOPSIS

Count the number of open Todo items in notes in the Journal folder.

.EXAMPLE
> Measure-JournalTodos

57 Todo Items in Journal

.EXAMPLE

This example requires go/chart/chart.go to be compiled and on the path.

> chart

 2.00 ┼  ╭
 1.00 ┤  │
 0.00 ┼──╯
#>
function Measure-JournalTodos() {
	$count = (minion.exe -todo | Measure-Object -Line).Lines
	$histFile = "~/.journal.task.count"

	if(Test-Path -Path $histFile) {
		$env:chart = Get-Content -Path $histFile
	}
	if ("$env:chart".Length -eq 0) {
		$env:chart = ""
	}
	Add-Content -Path $histFile -Value "|$count"
	$env:chart =  "$env:chart|$count"
	Write-Output "$count Todo Items in Journal"
}


function Get-JournalTodayTodos() {
	param(
		[int]$maximum = 20
	)
	minion.exe -todo -file "$(Get-JournalFile)" | Select-Object -Last $maximum
}

function Get-JournalAgenda() {
	param(
		[int]$maximum = 15
	)
	agenda.exe -path "$(Get-JournalFile)" | Select-Object -Last $maximum
}

Export-ModuleMember -Function Get-JournalTodos
Export-ModuleMember -Function Get-JournalTodayTodos
Export-ModuleMember -Function Measure-JournalTodos
Export-ModuleMember -Function Get-JournalAgenda
