package main

import (
	"encoding/csv"
	"fmt"
	"github.com/gocolly/colly/v2"
	"log"
	"os"
	"strings"
	"time"
)

func main() {
	start := time.Now()

	countyMap := map[string]int{
		"Florida":      69,
		"Alachua":      1,
		"Baker":        2,
		"Bay":          3,
		"Bradford":     4,
		"Brevard":      5,
		"Broward":      6,
		"Calhoun":      7,
		"Charlotte":    8,
		"Citrus":       9,
		"Clay":         10,
		"Collier":      11,
		"Columbia":     12,
		"Miami-Dade":   13,
		"DeSoto":       14,
		"Dixie":        15,
		"Duval":        16,
		"Escambia":     17,
		"Flagler":      18,
		"Fanklin":      19,
		"Gadsden":      20,
		"Gilchrist":    21,
		"Glades":       22,
		"Gulf":         23,
		"Hamilton":     24,
		"Hardee":       25,
		"Hendry":       26,
		"Hernando":     27,
		"Highlands":    28,
		"Hillsborough": 29,
		"Holmes":       30,
		"India River":  31,
		"Jackson":      32,
		"Jefferson":    33,
		"Lafayette":    34,
		"Lake":         35,
		"Lee":          36,
		"Leon":         37,
		"Levy":         38,
		"Liberty":      39,
		"Madison":      40,
		"Manatee":      41,
		"Marion":       42,
		"Martin":       43,
		"Monroe":       44,
		"Nassau":       45,
		"Okaloosa":     46,
		"Okeechobee":   47,
		"Orange":       48,
		"Osceola":      49,
		"Palm Beach":   50,
		"Pasco":        51,
		"Pinellas":     52,
		"Polk":         53,
		"Putnam":       54,
		"St. Johns":    55,
		"St. Lucie":    56,
		"Santa Rosa":   57,
		"Sarasota":     58,
		"Seminole":     59,
		"Sumter":       60,
		"Suwannee":     61,
		"Taylor":       62,
		"Union":        63,
		"Volusia":      64,
		"Wakulla":      65,
		"Walton":       66,
		"Washington":   67,
	}
	years := []int{2015, 2016, 2017, 2018, 2019, 2020, 2021}
	var urls []string
	var allData [][]string
	var finalHeaders []string

	for county_name, county_key := range countyMap {
		for _, year := range years {
			urls = append(urls, buildUrls(county_key, county_name, year))
		}
	}
	for _, url := range urls {
		newData, newHeaders := scrape(url)
		for _, row := range newData {
			allData = append(allData, row)
		}
		finalHeaders = newHeaders
	}
	writeFile(allData, finalHeaders)

	elapsed := time.Since(start)
	log.Printf("Scraping took %s", elapsed)
}

func buildUrls(countyCode int, county string, year int) string {
	baseUrl := fmt.Sprint("http://www.flhealthcharts.com/ChartsReports/rdPage.aspx?rdReport=SubstanceUseDashboard.SubstanceUseReport&ddlCounty=", countyCode, "&ddlYear=", year, "&selTab=1")
	return baseUrl
}

func scrape(baseUrl string) ([][]string, []string) {
	var headers []string
	var data []string
	var rows [][]string

	c := colly.NewCollector()

	c.OnError(func(_ *colly.Response, err error) {
		log.Println("Something went wrong:", err)
	})

	c.OnRequest(func(r *colly.Request) {
		fmt.Println("Visiting ->", baseUrl)
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
	})

	err := c.Visit(baseUrl)
	checkError("Failed to visit site", err)

	return rows, headers
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
	for _, value := range data {
		cleanRow := make([]string, len(value))
		for i, val := range value {
			cleanRow[i] = strings.TrimSpace(val)
		}
		tabularData = append(tabularData, cleanRow)
	}

	file, err := os.Create("results.csv")
	checkError("Cannot create file.", err)
	defer file.Close()

	writer := csv.NewWriter(file)
	defer writer.Flush()

	err2 := writer.WriteAll(tabularData)
	checkError("Cannot write to file", err2)
}

func checkError(message string, err error) {
	if err != nil {
		log.Fatal(message, err)
	}
}
