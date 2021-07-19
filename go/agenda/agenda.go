package main

import (
	"bufio"
	"flag"
	"fmt"
	"os"
	"regexp"
)

func searchForMatchesByLine(tagRegex regexp.Regexp, fileName string) []string {

	file, err := os.Open(fileName)
	if err != nil {
		fmt.Printf("Unable to read file: %s - %s", fileName, err)
	}
	scanner := bufio.NewScanner(file)
	var results = []string{}
	var result = []string{}
	for scanner.Scan() {
		result = tagRegex.FindAllString(scanner.Text(), -1)
		results = append(results, result...)
	}

	return results
}

func main() {
	agendaFile := flag.String("path", "", "Search this file agenda lines.")
	// maxFlag := flag.Int("max", 5, "Maximum number of lines to list.")
	flag.Parse()

	agendaRegex, _ := regexp.Compile(`(^\+\W[\d.]+\W[ap]m.+$)`) // How we find agenda items.

	var found = []string{}
	found = searchForMatchesByLine(*agendaRegex, *agendaFile)
	// TODO: Add a flag the removes line breaks, to allow files to be passed to Vim
	fmt.Println(found)
	fmt.Println()

}
