package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/url"
	"path/filepath"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/iam"
)

type AssumeRolePolicy struct {
	Version   string
	Statement json.RawMessage `json:"Statement"`
}

type Condition struct {
	StringEquals map[string]interface{}
	StringLike   map[string]interface{}
}

type Statement struct {
	Effect    string
	Action    string
	Principal struct {
		Service string
	}
	Condition Condition
}

type Results struct {
	Version   string
	Statement []Statement
}

func checkAssumeRolePolicy(assumeRolePolicy string, serviceAccount string, namespace string) {

	jsonResponse := []byte(assumeRolePolicy)

	res := &Results{}
	err := json.Unmarshal([]byte(jsonResponse), res)
	if err != nil {
		log.Fatal(err)
	}

	strictString := res.Statement[0].Condition.StringEquals
	nonstrictString := res.Statement[0].Condition.StringLike
	fullSa := fmt.Sprintf("system:serviceaccount:%s:%s", namespace, serviceAccount)

	if strictString != nil {
		for _, val := range strictString {
			//fmt.Println(key)
			fmt.Println(val)
		}
	} else {

		for _, val := range nonstrictString {

			fmt.Println(val)
			matched, _ := filepath.Match(val.(string), fullSa)

			if matched == true {
				fmt.Println("\U00002705 Service Account Regex Matched")
			} else {
				fmt.Println("\U0000274c Service Account Regex did not match")

			}
		}
	}

}

func compareAssumeRolePolicy(roleName string, serviceAccount string, namespace string) {
	cfg, err := config.LoadDefaultConfig(context.TODO())

	if err != nil {
		log.Fatalf("Error: %v", err)
	}

	client := iam.NewFromConfig(cfg)

	role := &iam.GetRoleInput{
		RoleName: &roleName,
	}

	roleOutput, err := client.GetRole(context.TODO(), role)

	if err != nil {
		panic(err)
	} else {
		result, _ := url.PathUnescape(*roleOutput.Role.AssumeRolePolicyDocument)
		checkAssumeRolePolicy(result, serviceAccount, namespace)
	}
}
