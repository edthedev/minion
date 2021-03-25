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
		[int]$max
	)
	if($max > 0) {
		minion.exe -todo | Select-Object -First $max
	}
	else {
		minion.exe -todo 
	}
}

function Measure-JournalTodos() {
		minion.exe -todo | Measure-Object -Line
}

Export-ModuleMember -Function Get-JournalTodos
Export-ModuleMember -Function Measure-JournalTodos
