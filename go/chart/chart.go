package main

import (
    "fmt"
		"flag"
		"os"
    "github.com/guptarohit/asciigraph"
		"math"
		"strings"
		"strconv"
)

func main() {
	flag.Parse()

	data := []float64{0,0}

	// Pull data from the environment variable.
	datastring := os.Getenv("chart")
	if (datastring == "") {
		datastring = "1|2|3|4|3|2|1"
	}
	fmt.Println(datastring)
	strData := strings.Split(datastring, "|")

	// Turn it into numbers.
	var item string
	var bigItem float64 = 0
	for _, item = range strData {
		dataItem,_ := strconv.ParseFloat(item, 32)
		if(dataItem > bigItem) {
			bigItem = dataItem
		}
		data = append(data, dataItem)
	}
	fmt.Println(data)
	// fmt.Println("Big Item ", bigItem)

	// Clean it for display size.
	sizedData := []float64{}
	var scaleFactor float64 = 1
	if(bigItem > 50) {
		scaleFactor = 10
	} else if bigItem > 20 {
		scaleFactor = 5
	} else if bigItem > 10 {
		scaleFactor = 2
	} else {
		scaleFactor = 1
	}
	fmt.Println("Chart scale is", scaleFactor)
	for _, dataItem := range data {
		sizedData = append(sizedData, math.Floor(dataItem / scaleFactor) )
	}

	graph := asciigraph.Plot(sizedData)
	fmt.Println(graph)
}