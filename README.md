# kubectl-irsa

This kubectl plugin allows us to test abilities of IAM policies which is assigned to the serviceAccount roles via AWS IAM Policy simulator service.
Beside of the IAM Policy Simulator it checks the other essential parts like this;

* Policy Simulator 🟢
* WebIdentity Issue 🟢
* Principal Checks 🟢
* OIDC linking issues like non existing IdentityProvider or wrong audience .. etc 🟠
* AdmissionController Check 🟠
* Thumbprint Check 🟠


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
  $ kubectl irsa -file config.yaml -sa application-service-account -namespace development
```
:warning: <b> Important </b>

Based on the latest Kubernetes version changes especially on AWS EKS, you may face issues with authentication API versions that's why you have to upgrade your AWS CLI V2 version while authenticating via IAM to connect the cluster.

<a href="https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html">How to upgrade awscli version</a>


## ConfigurationDetails

| flag | Description |
| --- | ----------- |
| role | Name of the role which assumed by service account which is assigned into the annotations of `eks.amazonaws.com/role-arn`  |
| config | Resource map configuration file |

## Setup 

### From Source;

This is a simple pip3 package so if you want to install this plugin on your cluster you just need to run this command like this;

```sh
    go build ./
    mv kubectl-irsa $PATH:/usr/local/bin
```

### Download
You can download plugin artifact over there;

https://github.com/TeamBion/kubectl-irsa/releases

# Contribution

More than welcome! please don't hesitate to open bugs, questions, pull requests