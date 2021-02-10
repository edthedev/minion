package main

import (
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"os"
	"path/filepath"
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

func main() {

	listFlag := flag.Bool("list", false, "List the files.")
	flag.Parse()

	var rootPath string = `C:\Users\delaport\Journal`
	var notMarkdown int = 0
	var matchCount int = 0

	fmt.Printf("List: %t, Find: %s", *listFlag, "...garbage...")

	if *listFlag {
		var results = []string{}

		fmt.Println("Aardvark.")
		walkErr := filepath.Walk(rootPath, func(path string, info os.FileInfo, err error) error {

			fmt.Println("Doggie.")
			if filepath.Ext(path) != ".md" {
				notMarkdown += 1
				return nil
			}

			found := searchInFile(path, "test")
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

		if(matchCount > 5) {
			fmt.Printf("Found %d matches.", matchCount)
		} else {
			fmt.Println(results)
		}


	}

	/*
		files, err := ioutil.ReadDir("c:\\src\\minion")
		if err != nil {
			log.Fatal(err)
		}

		for _, f := range files {
			fmt.Println(f.Name())
		}
	*/

}
