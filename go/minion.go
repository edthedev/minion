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
		fmt.Printf("Unable to read file: %s", fileName)
	}

	fileContent := string(data)

	found = strings.Contains(fileContent, searchString)
	return found

}

func main() {

	listFlag := flag.Bool("list", false, "List the files.")
	flag.Parse()

	var rootPath string = `C:\Users\edthe\Journal`

	fmt.Printf("List: %t, Find: %s", *listFlag, "...garbage...")

	if *listFlag {
		var results = []string{}

		var err error
		err = filepath.Walk(rootPath, func(path string, info os.FileInfo, err error) error {
			// println(info.Name())

			found := searchInFile(path, "test")
			if found {
				results = append(results, path)
			}

			return nil
		})

		fmt.Println(results)

		if err != nil {
			log.Fatal(err)
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
