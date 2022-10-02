package main

import (
	"fmt"
	"io/ioutil"
	"log"

	"gopkg.in/yaml.v2"
)

func (irsa *IRSAObject) parseYaml(configFile string) *IRSAObject {
	yamlFile, err := ioutil.ReadFile(configFile)

	if err != nil {
		fmt.Println(err)
	}

	err = yaml.Unmarshal(yamlFile, irsa)

	if err != nil {
		log.Fatalf("Unmarshal: %v", err)
	}
	return irsa

}
