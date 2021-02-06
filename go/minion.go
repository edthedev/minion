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

	fmt.Printf("List: %s, Find: %s", *listFlag, "...garbage...")

	if *listFlag {
		var err error
		err = filepath.Walk("c:\\src\\minion", func(path string, info os.FileInfo, err error) error {
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
