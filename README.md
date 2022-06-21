# kubectl-irsa

This kubectl plugin allows us to test abilities of IAM policies which is assigned to the serviceAccount roles via AWS IAM Policy simulator service.
Beside of the IAM Policy Simulator it checks the other essential parts like this;

* OIDC linking issues like non existing IdentityProvider or wrong audience .. etc 🟢
* Principal Checks 🟢
* WebIdentity Issue 🟢
* Policy Simulator 🟢

* Thumbprint Check 🟠
* AdmissionController Check 🟠 

## How to use ?

First step you have to create a simple resource and action map YAML file like this;

This yaml file contains resource list and related actions which would be possibly using by the serviceaccounts roles.

<b>Notice:</b> Each action simulates by the client on individual resources

```yaml
resources:
  - arn:aws:s3:::my-org-cdn-bucket
actions:
  - s3:DeleteBucket

```

After you create this yaml file you are able to use this like this

```sh
  $ kubectl irsa --config config.yaml --sa application-service-account --namespace development
```

## Usage

<img src="./img/main.gif"></img>

## Flags

| flag | Description |
| --- | ----------- |
| role | Name of the role which assumed by service account which is assigned into the annotations of `eks.amazonaws.com/role-arn`  |
| config | Resource map configuration file |
| clusterName | Name of the target cluster to check the OIDC related configurations|

## Setup 

This is a simple pip3 package so if you want to install this plugin on your cluster you just need to run this command like this;

```sh
    git clone git@github.com:WoodProgrammer/kubectl-irsa.git

    pip3 install . --upgrade
```

## Respect To 

### Bir Gün Sabah Sabah-Bir Turgut Uyar

<br>

[![IMAGE ALT TEXT HERE](https://img.youtube.com/vi/BuaDTTH4718/0.jpg)](https://www.youtube.com/watch?v=BuaDTTH4718)
