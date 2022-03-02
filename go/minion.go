package main

import (
	"bufio"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"regexp"
	"strings"
)

func searchInFile(fileName string, searchString string) bool {
	var found bool

	data, err := ioutil.ReadFile(fileName)
	if err != nil {
		fmt.Printf("Unable to read file: %s - %s", fileName, err)
	}

	fileContent := string(data)

	found = strings.Contains(fileContent, searchString)
	return found

}

func searchForTags(tagRegex regexp.Regexp, fileName string) []string {

	data, err := ioutil.ReadFile(fileName)
	if err != nil {
		fmt.Printf("Unable to read file: %s - %s", fileName, err)
	}
	fileContent := string(data)

	return tagRegex.FindAllString(fileContent, -1)
}

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

	searchFlag := flag.String("search", "", "Text to search for.")
	listFlag := flag.Bool("tags", false, "List any tags that look like [<text>].")
	todoFlag := flag.Bool("todo", false, "List any todo lines.")
	todoFile := flag.String("file", "", "Only search this file for todo lines.")
	// doneFlag := flag.Bool("done", false, "List any done lines.")
	maxFlag := flag.Int("max", 5, "Maximum number of files or tags to list.")
	flag.Parse()

	tagRegex, _ := regexp.Compile(`\[\S\S+\]`)          // How we find tags.
	todoRegex, _ := regexp.Compile(`(^\-\W\[\W+\].+$)`) // How we find todos
	// doneRegex, _ := regexp.Compile(`\[x\]|\[\/\]`) // How we find done items.

	var rootPath string = `C:\Users\delaport\Journal\2021`
	var notMarkdown int = 0
	var matchCount int = 0

	// fmt.Printf("List: %t, Find: %s.", *listFlag, *searchFlag)
	// fmt.Printf("List: %t, Find: %s.", "--default to list--", *searchFlag)
	// fmt.Println("")

	if *todoFile != "" {
		rootPath = *todoFile
	}

	if *listFlag {
		walkErr := filepath.Walk(rootPath, func(path string, info os.FileInfo, err error) error {

			if filepath.Ext(path) != ".md" {
				notMarkdown += 1
				return nil
			}

			var found = []string{}
			found = searchForTags(*tagRegex, path)
			// TODO: Add a flag the removes line breaks, to allow files to be passed to Vim
			fmt.Println(found)

			/*
				if found {
					// fmt.Printf("Found a match in: %s", path)
					matchCount += 1
					results = append(results, path)
				} else {
					// fmt.Printf("Found no match in: %s", path)
				}
			*/

			return nil
		})

		if walkErr != nil {
			log.Fatal(walkErr)
		}
	}

	if *todoFlag {
		walkErr := filepath.Walk(rootPath, func(path string, info os.FileInfo, err error) error {

			if filepath.Ext(path) != ".md" {
				notMarkdown += 1
				return nil
			}

			var found = []string{}
			found = searchForMatchesByLine(*todoRegex, path)
			// fmt.Println(found)
			var todo string

			if len(found) > 0 {
				fmt.Println("## ", path)
				fmt.Println("")
			}
			for _, todo = range found {
				fmt.Println(todo)
				fmt.Println("")
			}

			/*
				if found {
					// fmt.Printf("Found a match in: %s", path)
					matchCount += 1
					results = append(results, path)
				} else {
					// fmt.Printf("Found no match in: %s", path)
				}
			*/

			return nil
		})

		if walkErr != nil {
			log.Fatal(walkErr)
		}
	}

	if *searchFlag != "" {
		var results = []string{}

		walkErr := filepath.Walk(rootPath, func(path string, info os.FileInfo, err error) error {

			if filepath.Ext(path) != ".md" {
				notMarkdown += 1
				return nil
			}

			found := searchInFile(path, *searchFlag)
			if found {
				// fmt.Printf("Found a match in: %s", path)
				matchCount += 1
				results = append(results, path)
			} else {
				// fmt.Printf("Found no match in: %s", path)
			}

			return nil
		})
		if walkErr != nil {
			log.Fatal(walkErr)
		}
		// fmt.Printf("Skipped %d non markdown (.md) files. ", notMarkdown)

		if matchCount > *maxFlag {
			fmt.Printf("Found %d matches.", matchCount)
		} else {
			for _, item := range results {
				// fmt.Println(item)
				// Print space separated for Vim command line input.
				// var escaped string
				// escaped = strings.Replace(item, `\`, "/", -1)
				fmt.Printf("%s ", item)
			}
			// fmt.Println(results)
		}

	}

}
