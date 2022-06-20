import boto3
import logging

class EKS(object):

    def __init__(self):
        self.eks_client = boto3.client("eks")

    def checkOIDC(self, config):
        clusterName = config["eks"]["clusterName"]

        try:
            oidcRaw = self.eks_client.list_identity_provider_configs(clusterName=clusterName)
            status = oidcRaw["identityProviderConfigs"]
            if len(status) == 0:
                decisionEmoji = "\U0000274c"
            else:
                decisionEmoji = "\U00002705" 

            print("OIDC Definition status is - {} ".format(decisionEmoji))

        except Exception as exp:
            logging.error(exp)