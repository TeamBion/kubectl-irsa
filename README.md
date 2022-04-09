# kubeirsa
This is a sample project that allows us to test IAM IRSA policy capabilities.

## Example Usage; 

* Functional Test with local-stack.

<code>
kubectl irsa --policy-file policy.json --type  functional
</code>

* Integration Test with AWS API

<code>
kubectl irsa --policy-file policy.json --type integration --service-account application-service-account
</code>

Expected output is ;

aws sts results : OK :green-mark: or FALSE :danger: 
ERROR check the Identity

