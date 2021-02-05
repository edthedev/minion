package main

import (
	"fmt"
	"github.com/docopt/docopt-go"
)

func main() {
	  usage := `Minion. Your command line personal assistance.

Usage:
	minion tags - list all tags
	minion list - list all files matching keywords
	minion -h | --help
  minion --version

Options:
  -h --help     Show this screen.
  --version     Show version.
	-d --days=<days>         Show notes modified last N days .
	-m --max=<max>           Maximum results to display. [default: 10]
	-y --year=<year>         Limit results to those created in the given year. [default: current year]`

		arguments, _ := docopt.ParseDoc(usage)
	  fmt.Println(arguments)
}
