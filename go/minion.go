package main

import (
	"fmt"
	"github.com/docopt/docopt-go"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
)

func main() {
	usage := `Minion. Your command line personal assistance.

Usage:
	minion tags - list all tags
	minion list - list all files matching keywords
	minion find <text> - list all files matching keywords
	minion -h | --help
  minion --version

Options:
  -h --help     Show this screen.
  --version     Show version.
	-d --days=<days>         Show notes modified last N days .
	-m --max=<max>           Maximum results to display. [default: 10]
	-y --year=<year>         Limit results to those created in the given year. [default: current year]`

	var conf struct {
		Tags bool
		List bool
		Find []string
		Max  int
		Year int
		Days int
	}
	opts, _ := docopt.ParseDoc(usage)
	// fmt.Println(arguments)

	opts.Bind(&conf)

	if conf.List {
		var err error
		err = filepath.Walk("c:\\src\\minion", func(path string, info os.FileInfo, err error) error {
			println(info.Name())
			return nil
		})
		if err != nil {
			log.Fatal(err)
		}
	}

	if conf.Tags {

		files, err := ioutil.ReadDir("c:\\src\\minion")
		if err != nil {
			log.Fatal(err)
		}

		for _, f := range files {
			fmt.Println(f.Name())
		}
	}

}
