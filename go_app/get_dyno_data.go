package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
	"os/exec"
)

func get_dyno_data(days string) (int, int, float32) {
	// type Sentidata struct {
	// 	U float32
	// 	N float32
	// 	S float32
	// }
	type Sentidata struct {
		Positive_counter float32
		Negative_counter float32
		Stock_counter    float32
	}

	logFile := setLogfile("get-dyno-go.log")
	log.SetOutput(logFile)
	log.Println("get dyno log file created")

	cmd := exec.Command("./read_dyanmodb.py", days)
	if err := cmd.Run(); err != nil {
		log.Println(err)
		return 0, 0, 0
	}

	// read file
	data, err := ioutil.ReadFile("./dynamodata.json")
	if err != nil {
		fmt.Print(err)
	}

	// json data
	var obj Sentidata

	// unmarshall it
	err = json.Unmarshal(data, &obj)
	if err != nil {
		fmt.Println("error:", err)
	}
	fmt.Println(data, obj)
	// can access using struct now
	// fmt.Printf("u : %.2f\n", obj.Positive_counter)
	// fmt.Printf("N : %.2f\n", obj.Negative_counter)
	// fmt.Printf("s : %.2f\n", obj.Stock_counter)

	return int(obj.Positive_counter), int(obj.Negative_counter), obj.Stock_counter
}
