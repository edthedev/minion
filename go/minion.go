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

	fmt.Printf("List: %t, Find: %s", *listFlag, "...garbage...")

	if *listFlag {
		// var results = []string{}

		fmt.Println("Aardvark.")
		walkErr := filepath.Walk(rootPath, func(path string, info os.FileInfo, err error) error {
			fmt.Println("Bobcat.")
			/*if(info == nil){
				fmt.Printf("Info nil at %s", path)
				return nil
			}*/

			/*
			fmt.Println("Catterpillar.")
			if(info.IsDir()) {
				fmt.Printf("Is a directory: %s", path)
				return nil
			}*/

			fmt.Println("Doggie.")
			if filepath.Ext(path) != ".md" {
				// fmt.Printf("Is not markdown: %s", path)
				notMarkdown += 1
				return nil
			}

			fmt.Println("Elephant.")
			found := searchInFile(path, "test")
			fmt.Println("Fly.")
			if found {
				fmt.Printf("Found a match in: %s", path)
				// results = append(results, path)
			} else {
				fmt.Printf("Found no match in: %s", path)
			}
			fmt.Println("Housefly.")

			return nil
		})
		if walkErr != nil {
			log.Fatal(walkErr)
		}
		fmt.Printf("Is not markdown: %d", notMarkdown)

		// fmt.Println(results)

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
