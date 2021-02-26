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

$dataFile = "~/panel.json"

function Invoke-Panel() {
	param(
		[string]$Path = "~/panel.json"
	)

	$toolbar = Get-PanelToolbar
	$data = Get-PanelData -Path $path
	$cmd = Read-Host -Prompt $toolbar
	$done = ($cmd -eq "x")
	while(-Not $done){

		Show-PanelData -Data $data -View 1

		Write-Host "Huzzah!"
		$cmd = Read-Host -Prompt $toolbar
		$done = ($cmd -eq "x")
	}
	Write-Host "Finished."
}
function Get-PanelToolbar() {
	return "e - Edit, p - Previous, n - Next, x - Exit"
}

<#
.SYNOPSIS

Load data from file.

#>
function Get-PanelData() {
	param(
		[string]$Path = "~/panel.json"
	)
	if(Test-Path -Path $path) {
		$data = (Get-Content -Path $path) | Convert-FromJson
		return $data
	}
	return Get-PanelTemplate
}
function Set-PanelData() {
	# return Get-Content -Path $dataFile | Convert-FromJson
	Write-Host "Oops. Not implemented."
}

enum PanelViews {
	WELCOME = 1
	LIST1
	LIST2
	LIST3
}
<#
.SYNOPSIS

Show selected view.

#>
function Show-PanelData() {
	param(
		[string]$data,
		[int]$view
	)
	"Showing panel $view"
	$display = Switch ($view)
	{
		PanelViews.WELCOME { "Welcome" }
		PanelViews.LIST1 { "List 1!" }
		PanelViews.LIST2 { "List 2!" }
		PanelViews.LIST3 { "List 3!" }
	}
  Write-Host $display
}

function Get-PanelTemplate() {
$template = @'
{
	lists: [
	['Shopping', 'Eggs', 'Milk'],
	['TODO', 'Try out this cool tool.']
]
}
'@
return $template
}
function Get-PanelMarkdown() {

}
Export-ModuleMember -Function Invoke-Panel
