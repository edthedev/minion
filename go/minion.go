package main

import (
	"flag"
	"fmt"

	// "io/ioutil"
	"log"
	"os"
	"path/filepath"
)

func searchInFile(fileName string, searchString string) {
	var found bool

	data, err := ioutil.ReadFile(fileName)
	if err != nil {
		fmt.Printf("Unable to read file: %s", fileName)
	}

	fileContent := string(data)

	found = strings.contains(fileContent, searchString)
	return found

}

func main() {

	listFlag := flag.Bool("list", false, "List the files.")
	flag.Parse()

	var rootPath string = `C:\Users\edthe\Journal`

	fmt.Printf("List: %t, Find: %s", *listFlag, "...garbage...")

	if *listFlag {
		var results := []str{}

		var err error
		err = filepath.Walk(rootPath, func(path string, info os.FileInfo, err error) error {
			// println(info.Name())

			if searchInFile(info.path, "test") {
				results.append(info.path)
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
