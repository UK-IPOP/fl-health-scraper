package main

import (
	"encoding/csv"
	"fmt"
	"log"
	"os"
	"strings"
	"time"

	"github.com/gocolly/colly/v2"
)

func main() {
	start := time.Now()

	var headers []string
	var data []string
	var rows [][]string

	c := colly.NewCollector(
		colly.Async(true),
	)
	c.SetRequestTimeout(50 * time.Second)
	limitErr := c.Limit(&colly.LimitRule{
		DomainGlob:  "*",
		Parallelism: 10,
		Delay:       1 * time.Second,
		RandomDelay: 3 * time.Second,
	})
	if limitErr != nil {
		checkError("Could not handle parallel limiter.", limitErr)
	}

	c.OnError(func(r *colly.Response, err error) {
		log.Println("Something went wrong:", err)
	})

	c.OnRequest(func(r *colly.Request) {
		fmt.Println("Visiting ->", r.URL)
	})

	c.OnResponse(func(r *colly.Response) {
		fmt.Println("Visited:", r.Request.URL)
	})

	c.OnHTML("#dtSubstanceUse thead tr th", func(e *colly.HTMLElement) {
		if len(headers) <= 8 {
			headers = append(headers, e.Text)
		}
	})

	c.OnHTML("#dtSubstanceUse tbody tr[row] td", func(e *colly.HTMLElement) {
		data = append(data, e.Text)
	})

	c.OnScraped(func(r *colly.Response) {
		// split data into 8 segments
		rows = append(rows, segmentData(data)...)
	})

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
	urls := buildUrls(countyMap, years)

	for _, url := range urls {
		err := c.Visit(url)
		if err != nil {
			checkError(fmt.Sprintf("Error on url: %s", url), err)
		}
	}

	c.Wait()
	elapsed := time.Since(start)
	log.Printf("Scraping took %s", elapsed)
	log.Println("Writing to file.")
	writeFile(rows, headers)
	log.Println("Done.")
}

func buildUrls(countyCodes map[string]int, years []int) []string {
	var urls []string
	for _, code := range countyCodes {
		for _, year := range years {
			url := fmt.Sprint("http://www.flhealthcharts.com/ChartsReports/rdPage.aspx?rdReport=SubstanceUseDashboard.SubstanceUseReport&ddlCounty=", code, "&ddlYear=", year, "&selTab=1")
			urls = append(urls, url)
		}
	}
	return urls
}

func segmentData(data []string) [][]string {
	var rows [][]string

	for i := 0; i < len(data); i += 8 {
		row := data[i : i+8]
		rows = append(rows, row)
	}
	subsetRows := rows[1:5]
	subsetRows = append(subsetRows, rows[6:16]...)
	subsetRows = append(subsetRows, rows[17:]...)
	return subsetRows
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
	writer := csv.NewWriter(file)
	err2 := writer.WriteAll(tabularData)
	checkError("Cannot write to file", err2)
	defer func() {
		writer.Flush()
		if err := file.Close(); err != nil {
			checkError("Failed to flush file.", err)
		}
	}()
}

func checkError(message string, err error) {
	if err != nil {
		log.Fatal(message, err)
	}
}
