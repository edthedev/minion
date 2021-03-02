## What is Minion?

[![Build Status](https://travis-ci.org/edthedev/minion.svg?branch=develop)](https://travis-ci.org/edthedev/minion)

Minion automates the boring parts of file management to let authors focus on writing. Deciding what to name a file, where to put it, and trying to find it later are all steps that can be delegated - to Minion.

## The Philosophy of Minion 

In Vernor Vinge's novel, 'The Peace War', chess players can instantly upload thoughts from their minds into a computer for storage, and then recover and act on those thoughts later. 

Minion is meant to be a first step on that path. Minion simplifies storing, tagging, and retrieving ideas, freeing it's user to focus on thinking.

## Why Minion?

1. Capture thoughts in the moment. The note function gets an editor open to capture thoughts quickly.
2. Take next steps. Convert captured ideas into actions and artifacts. The sort function makes it simple to review files and take next steps related to them.
3. Never lose anything. The find, open and archive commands make sure that files are only a few keypresses away.
4. Keep track of upcoming dates. The dates function displays recent and upcoming date strings that appear in files.

## Installation

+ Install PowerShell.
+ Clone the source.
+ See `profiles` and `psmodules` for PowerShell integration.
+ Optionally compile `go/minion.go` for additional search capabilities.

## Usage

After setting up your PowerShell profile to import the module: 

```powershell
C:\src\minion\psmodule [cleanup +0 ~1 -0 !]> get-command -Module minion

CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Function        Get-JournalFile                                    0.0        minion
Function        Get-JournalNote                                    0.0        minion
Function        Get-JournalToday                                   0.0        minion
Function        Get-JournalTomorrow                                0.0        minion
Function        Get-JournalYesterday                               0.0        minion
```

```powershell
Get-Help Invoke-JournalNote
```

