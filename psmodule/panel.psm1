#!/usr/bin/pwsh

<#
.SYNOPSIS

Quick notes stored in a pre-defined JSON file.

.EXAMPLE

> Invoke-Panel

.NOTES

This is a quick opinionated digital notebook for
notes you do not need to keep for long.

Recommended for your PowerShell profile:

> Import-Module c:\src\minion\modules\panel.psm1
> New-Alias panel Invoke-Panel

See profile/alias.ps1 for more examples.

#>

function Invoke-Panel() {
	param(
		[string]$Path = "~/panel.json"
	)

	$toolbar = Get-PanelToolbar
	$cmd = Read-Host -Prompt $toolbar
	$done = ($cmd -eq "x")
	while(-Not $done){
		Write-Host "Huzzah!"
		$cmd = Read-Host -Prompt $toolbar
		$done = ($cmd -eq "x")
	}
	Write-Host "Finished."
}
function Get-PanelToolbar() {
	return "e - Edit, p - Previous, n - Next, x - Exit"
}

function Get-PanelTemplate() {
$template = @'
{

}
'@
return $template
}
function Get-PanelMarkdown() {

}
Export-ModuleMember -Function Invoke-Panel
