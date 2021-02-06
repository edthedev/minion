package main

import (
	"flag"
	"fmt"

	// "io/ioutil"
	"log"
	"os"
	"path/filepath"
)

func main() {

	listFlag := flag.Bool("list", false, "List the files.")
	flag.Parse()

	var rootPath string = `C:\Users\edthe\Journal`

	fmt.Printf("List: %t, Find: %s", *listFlag, "...garbage...")

	if *listFlag {
		var err error
		err = filepath.Walk(rootPath, func(path string, info os.FileInfo, err error) error {
			println(info.Name())
			return nil
		})
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
