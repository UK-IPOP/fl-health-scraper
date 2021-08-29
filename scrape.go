package main

import (
	"encoding/csv"
	"fmt"
	"github.com/gocolly/colly/v2"
	"log"
	"os"
	"strings"
)

func main() {
	baseUrl := "http://www.flhealthcharts.com/ChartsReports/rdPage.aspx?rdReport=SubstanceUseDashboard.SubstanceUseReport&ddlCounty=69&ddlYear=2021&selTab=1"
	var headers []string
	var data []string
	var rows [][]string

	c := colly.NewCollector()

	c.OnError(func(_ *colly.Response, err error) {
		log.Println("Something went wrong:", err)
	})

	c.OnRequest(func(r *colly.Request) {
		fmt.Println("Visiting", r.URL)
	})

	c.OnHTML("#dtSubstanceUse thead tr th", func(e *colly.HTMLElement) {
		headers = append(headers, e.Text)
	})

	c.OnHTML("#dtSubstanceUse tbody tr[row] td", func(e *colly.HTMLElement) {
		data = append(data, e.Text)
	})

	c.OnScraped(func(r *colly.Response) {
		// split data into 8 segments
		rows = splitData(data)
		writeFile(rows, headers)
		fmt.Println("Finished", r.Request.URL)
	})

	err := c.Visit(baseUrl)
	checkError("Failed to visit site", err)
}

func splitData(data []string) [][]string {
	var rows [][]string

	for i := 0; i < len(data); i += 8 {
		row := data[i : i+8]
		rows = append(rows, row)
	}
	return rows
}

func writeFile(data [][]string, headers []string) {

	// bad version of inserting headers in 0 index
	var tabularData [][]string
	tabularData = append(tabularData, headers)
	for _, val := range data {
		tabularData = append(tabularData, val)
	}

	file, err := os.Create("results.csv")
	checkError("Cannot create file.", err)
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()
	for _, value := range data {
		cleanRow := make([]string, len(value))
		for i, val := range value {
			cleanRow[i] = strings.TrimSpace(val)
		}
		err := writer.Write(cleanRow)
		checkError("Cannot write to file", err)
	}
}

func checkError(message string, err error) {
	if err != nil {
		log.Fatal(message, err)
	}
}
