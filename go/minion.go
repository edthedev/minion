package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
	"strings"
	"regexp"
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


func searchForTags(tagRegex regexp.Regexp, fileName string) bool {
	var found bool
	

	data, err := ioutil.ReadFile(fileName)
	if err != nil {
		fmt.Printf("Unable to read file: %s - %s", fileName, err)
	}
	fileContent := string(data)

	fmt.Println(tagRegex.FindAllString(fileContent, -1))

	found = strings.Contains(fileContent, "NEVERMIND")
	return found

}


func main() {

	searchFlag := flag.String("search", "", "Text to search for.")
	listFlag := flag.Bool("tags", false, "List any tags that look like [<text>].")
	maxFlag := flag.Int("max", 5, "Maximum number of files or tags to list.")
	flag.Parse()
	tagRegex, _ := regexp.Compile("p([a-z]+)ch")

	var rootPath string = `C:\Users\delaport\Journal\2021`
	var notMarkdown int = 0
	var matchCount int = 0

	fmt.Printf("List: %t, Find: %s.", *listFlag, *searchFlag)
	// fmt.Printf("List: %t, Find: %s.", "--default to list--", *searchFlag)
	fmt.Println("")
	if ( *listFlag ) {
		var results = []string{}

		walkErr := filepath.Walk(rootPath, func(path string, info os.FileInfo, err error) error {

			if filepath.Ext(path) != ".md" {
				notMarkdown += 1
				return nil
			}

			found := searchForTags(*tagRegex, path)
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
		fmt.Printf("Skipped %d non markdown (.md) files. ", notMarkdown)

		if(matchCount > *maxFlag) {
			fmt.Printf("Found %d matches.", matchCount)
		} else {
		  for _, item := range results {
				fmt.Println(item)
			}
			// fmt.Println(results)
		}

	}

	if (*searchFlag != "") {
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
		fmt.Printf("Skipped %d non markdown (.md) files. ", notMarkdown)

		if(matchCount > *maxFlag) {
			fmt.Printf("Found %d matches.", matchCount)
		} else {
		  for _, item := range results {
				fmt.Println(item)
			}
			// fmt.Println(results)
		}

	}

}
