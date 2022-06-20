import boto3
import logging

class EKS(object):

    def __init__(self):
        self.eks_client = boto3.client("eks")

    def oidcIssuerId(self, clusterName):
        cluster = self.eks_client.describe_cluster( name=clusterName)
        try:
            oidcId = cluster["cluster"]["identity"]["oidc"]["issuer"]
            oidcId = oidcId.replace("https://", "")
        except Exception as exp:
            logging.error(exp)
            oidcId = ""
        
        return oidcId