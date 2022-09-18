package main

type IRSAObject struct {
	Resource []string `yaml:"resources"`

	Actions []string `yaml:"actions"`
}
