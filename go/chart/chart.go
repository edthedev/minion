package main

import (
    "fmt"
		"flag"
		"os"
    "github.com/guptarohit/asciigraph"
		"strings"
		"strconv"
)

func main() {
	flag.Parse()

	data := []float64{0,0}

	datastring := os.Getenv("chart")
	if (datastring == "") {
		datastring = "1|2|3|4|3|2|1"
	}
	fmt.Println(datastring)
	strData := strings.Split(datastring, "|")

	var item string
	for _, item = range strData {
		dataItem,_ := strconv.ParseFloat(item, 32)
		data = append(data, dataItem)
	}
	fmt.Println(data)

	graph := asciigraph.Plot(data)
	fmt.Println(graph)
}