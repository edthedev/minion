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
		[int]$Max = 20
	)
	minion.exe -todo | Select-Object -Last $Max
}

function Measure-JournalTodos() {
	$count = (minion.exe -todo | Measure-Object -Line).Lines
	if($count -gt 10) {
		$data = [math]::Floor($count / 10)
	} else 
	{
		$data = $count
	}
	
	if ("$env:todochart".Length -eq 0) {
		$env:todochart = ""
	}
	$env:todochart += "|$data"
	Write-Output "$count Todo Items in Journal"
}

Export-ModuleMember -Function Get-JournalTodos
Export-ModuleMember -Function Measure-JournalTodos
