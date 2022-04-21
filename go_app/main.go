package main

import (
	"fmt"
	"html/template"
	"log"
	"net/http"
)

type Sentidata struct {
	Positive_sent int
	Negative_sent int
	Share_percent float32
	Time_period   string
	Stock_colour  string
	Stock_Text    string
}

var sentdata = Sentidata{
	Positive_sent: 0,
	Negative_sent: 0,
	Share_percent: 0.0,
	Time_period:   "Unknown",
	Stock_colour:  "grey",
	Stock_Text:    "??",
}

func check(err error) {
	if err != nil {
		log.Fatal(err)
	}
}
func viewHandler(writer http.ResponseWriter, request *http.Request) {

	html, err := template.ParseFiles("static/mvp2.html")
	check(err)
	err = html.Execute(writer, sentdata)
	check(err)
}

func testHandler(writer http.ResponseWriter, request *http.Request) {

	err := request.ParseForm()
	check(err)
	data := request.PostForm.Get("comp_select")
	day := "0"

	sentdata.Time_period = data
	if data == "1 day" {
		day = "1"
	} else if data == "1 week" {
		day = "7"
	} else if data == "1 month" {
		day = "30"
	} else if data == "1 year" {
		day = "365"
	} else {
		day = "0"
	}

	sentdata.Positive_sent, sentdata.Negative_sent, sentdata.Share_percent = get_dyno_data(day)
	if sentdata.Share_percent > 0 {
		sentdata.Stock_colour = "green"
		sentdata.Stock_Text = "Up "
	} else {
		sentdata.Stock_colour = "Tomato"
		sentdata.Stock_Text = "Down "
	}

	http.Redirect(writer, request, "/", 301)
}

func initSentData() {
	// from dynamodb, init it 1st run
	sentdata.Positive_sent, sentdata.Negative_sent, sentdata.Share_percent = get_dyno_data("1")
	if sentdata.Share_percent > 0 {
		sentdata.Stock_colour = "green"
		sentdata.Stock_Text = "Up "
	} else {
		sentdata.Stock_colour = "Tomato"
		sentdata.Stock_Text = "Down "
	}
	sentdata.Time_period = "1 Day"

}

func main() {
	initSentData()
	fmt.Println("Running on localhost 8080....")
	http.HandleFunc("/test", testHandler)
	http.HandleFunc("/", viewHandler)

	fs := http.FileServer(http.Dir("./static/"))
	http.Handle("/static/", http.StripPrefix("/static/", fs))

	err := http.ListenAndServe(":8080", nil)
	log.Fatal(err)
}
