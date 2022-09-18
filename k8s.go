package main

import (
	"context"
	"flag"
	"path/filepath"

	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/client-go/kubernetes"
	"k8s.io/client-go/tools/clientcmd"
	"k8s.io/client-go/util/homedir"
)

func parseRole(namespace string, targetAccount string) string {

	var kubeconfig *string
	var targetRole string

	if home := homedir.HomeDir(); home != "" {
		kubeconfig = flag.String("kubeconfig", filepath.Join(home, ".kube", "config"), "(optional) absolute path to the kubeconfig file")
	} else {
		kubeconfig = flag.String("kubeconfig", "", "absolute path to the kubeconfig file")
	}
	flag.Parse()

	config, err := clientcmd.BuildConfigFromFlags("", *kubeconfig)
	if err != nil {
		panic(err)
	}
	clientset, err := kubernetes.NewForConfig(config)
	if err != nil {
		panic(err)
	}

	data := clientset.CoreV1().ServiceAccounts(namespace)
	status, _ := data.Get(context.TODO(), targetAccount, metav1.GetOptions{})

	for index, annotation := range status.Annotations {
		if index == "eks.amazonaws.com/role-arn" {
			targetRole = annotation
		}
	}

	return targetRole
}
