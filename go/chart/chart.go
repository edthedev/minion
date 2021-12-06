package main

import (
	"flag"
	"fmt"
	"math"
	"os"
	"strconv"
	"strings"

	"github.com/guptarohit/asciigraph"
)

/*

C:\src\minion\go\chart [main ↑1]> $env:chart
|23|20|15|12|12|15|15|6|5|0

C:\src\minion\go\chart [main ↑1]> chart
[0 0 0 23 20 15 12 12 15 15 6 5 0]
Chart scale is 5
 4.00 ┼  ╭─╮
 3.00 ┤  │ ╰╮ ╭─╮
 2.00 ┤  │  ╰─╯ │
 1.00 ┤  │      ╰─╮
 0.00 ┼──╯        ╰

*/

func GetLatest(datastring string, max int) (res []string) {
	strData := strings.Split(datastring, "|")
	if len(strData) < max {
		return strData
	}
	return strData[len(strData)-max:]
}

func main() {
	envVar := flag.String("var", "chart", "Environment variable to chart from.")
	flag.Parse()

	data := []float64{0, 0}

	// Pull data from the environment variable.
	datastring := os.Getenv(*envVar)
	if datastring == "" {
		datastring = "|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15"
		datastring = datastring + "|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15"
		datastring = datastring + "|1|2|3|4|5|6|7|8|9|10|11|12|13|14|15"
	}
	strData := GetLatest(datastring, 73)

	// Turn it into numbers.
	var item string
	var bigItem float64 = 0
	for _, item = range strData {
		item = strings.TrimSpace(item)
		dataItem, _ := strconv.ParseFloat(item, 32)
		if dataItem > bigItem {
			bigItem = dataItem
		}
		data = append(data, dataItem)
	}
	// fmt.Println(data)

	// Clean it for display size.
	sizedData := []float64{}
	var scaleFactor float64 = 1
	if bigItem > 50 {
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
		sizedData = append(sizedData, math.Floor(dataItem/scaleFactor))
	}

	graph := asciigraph.Plot(sizedData)
	fmt.Println(graph)
}
