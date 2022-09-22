package main

import (
	"context"
	"flag"
	"fmt"
	"log"

	"github.com/aws/aws-sdk-go-v2/config"
	"github.com/aws/aws-sdk-go-v2/service/iam"
)

var (
	file           = flag.String("file", "", "config file that contains resource and permission list")
	namespace      = flag.String("namespace", "default", "Target Namespace")
	serviceAccount = flag.String("sa", "", "Target service account")
)

func main() {

	flag.Parse()

	var irsaObj IRSAObject

	configFile := *irsaObj.parseYaml(*file)

	actionList := []string{}
	resourceList := []string{}

	roleName := parseRole(*namespace, *serviceAccount)

	for _, action := range configFile.Actions {
		actionList = append(actionList, action)
	}

	for _, resource := range configFile.Resource {
		resourceList = append(resourceList, resource)
	}

	cfg, err := config.LoadDefaultConfig(context.TODO())
	if err != nil {
		log.Fatalf("Error: %v", err)
	}

	client := iam.NewFromConfig(cfg)

	policyInput := iam.SimulatePrincipalPolicyInput{
		ActionNames:     actionList,
		ResourceArns:    resourceList,
		PolicySourceArn: &roleName,
	}

	result, err := client.SimulatePrincipalPolicy(context.TODO(), &policyInput)

	if err != nil {
		log.Fatalf("Error: %v", err)
	} else {
		for _, result := range result.EvaluationResults {
			actionName := result.EvalActionName
			decisionName := result.EvalDecision

			if decisionName == "allowed" {
				fmt.Println("\U00002705 ", *actionName)
			} else {
				fmt.Println("\U0000274c ", *actionName)
			}

		}
	}

	compareAssumeRolePolicy(roleName)

}
