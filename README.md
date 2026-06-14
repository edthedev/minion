# Minion

## Archived

I have replaced this tool in my own workflow.

My work on Minion continues on CodeBerg at 
https://codeberg.org/EdTheDev/minion

The new version is almost entirely written in`bash` and has been tested on Linux Mint and MacOSX.

- For journaling and quick notes, I ~~recommend [VSCode Journal](https://marketplace.visualstudio.com/items?itemName=pajoma.vscode-journal).~~ now use [Minion](https://codeberg.org/EdTheDev), again.
- For finding `todo` items in my journal, I (still) use [my Go Todolist](https://github.com/edthedev/todolist).
- For a daily agenda view, I (still) use [my Go agenda tool](https://github.com/edthedev/agenda).

## What is Minion?

> (While this is an archive of the Python and PowerShell versions, most of this talk about vision will be roughly correct for the new [Bash version of Minion](
https://codeberg.org/EdTheDev).)

Minion automates the boring parts of file management to let authors focus on writing. Deciding what to name a file, where to put it, and trying to find it later are all steps that can be delegated - to Minion.

## The Philosophy of Minion

Minion simplifies storing, tagging, and retrieving ideas, freeing it's user to focus on thinking.
Minion is intentionally opinionated. Files are stored as Markdown. Todo is always indicated with `- [ ]`.
Minion is compatible with other tools that use Markdown files.

## Why Minion?

1. Capture thoughts in the moment. The note function gets an editor open to capture thoughts quickly.
2. Take next steps. Convert captured ideas into actions and artifacts.
3. Never lose anything. The find, open and archive commands make sure that files are only a few keypresses away.

## Installation

> (This is an atchive. Consider using [Minion for Bash](https://codeberg.org/EdTheDev), instead.


+ Install PowerShell and GoLang.
+ Clone the source.
+ See `profiles` and `psmodules` for PowerShell integration.
+ Compile `go/minion.go` for additional search capabilities.

## Usage

After setting up your PowerShell profile to import the module: 

```powershell
$ Get-Command -Module minion

CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Function        Get-JournalFile                                    0.0        minion
Function        Get-JournalNote                                    0.0        minion
Function        Get-JournalToday                                   0.0        minion
Function        Get-JournalTomorrow                                0.0        minion
Function        Get-JournalYesterday                               0.0        minion

$ Get-Command -Module minion_go

CommandType     Name                                               Version    Source
-----------     ----                                               -------    ------
Function        Get-JournalAgenda                                  0.0        minion_go
Function        Get-JournalTodayTodos                              0.0        minion_go
Function        Get-JournalTodos                                   0.0        minion_go
Function        Measure-JournalTodos                               0.0        minion_go
```

```powershell
Get-Help Invoke-JournalNote
```

