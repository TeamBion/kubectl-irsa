package main

import (
	"context"
	"encoding/json"
	"fmt"
	"log"
	"net/url"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/iam"
)

type AssumeRolePolicy struct {
	Version   string
	Statement json.RawMessage `json:"Statement"`
}

type Condition struct {
	StringEquals map[string]interface{}
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

func checkAssumeRolePolicy(assumeRolePolicy string) {

	jsonResponse := []byte(assumeRolePolicy)

	res := &Results{}
	err := json.Unmarshal([]byte(jsonResponse), res)
	if err != nil {
		log.Fatal(err)
	}
	hede := res.Statement[0].Condition.StringEquals

	for key, val := range hede {
		fmt.Println(key)
		fmt.Println(val)
	}

}

func compareAssumeRolePolicy(roleName string) {
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
		checkAssumeRolePolicy(result)
	}
}
