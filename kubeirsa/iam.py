import boto3
from eks import EKS

class IAM(object):

    def __init__(self):
        self.iam_client = boto3.client("iam")
        sts_client = boto3.client("sts")
        
        self.accountId = sts_client.get_caller_identity()["Account"]


    def checkOIDC(self, config):
        clusterName = config["clusterName"]

        eksObj = EKS()

        oidcId = eksObj.oidcIssuerId(clusterName)
        
        openIdProviders = self.iam_client.list_open_id_connect_providers()
        for openIdProvider in openIdProviders["OpenIDConnectProviderList"]:
            if openIdProvider["Arn"] == "arn:aws:iam::{}:oidc-provider/{}".format(self.accountId, oidcId):
                status = 1
                break
            else:
                status = 0

        if status == 1:
            decisionEmoji = "\U00002705"
        else:
            decisionEmoji = "\U0000274c"
        
        print("OIDC provider connectivity between IAM and EKS is :: {}".format(decisionEmoji ))


class IAMPolicySimulator(object):

    def __init__(self):
        self.iam_client = boto3.client("iam")

    def generateOutput(self, responseList):

        for response in responseList:

            evResource = response["EvaluationResults"][0]["EvalResourceName"]
            evAction = response["EvaluationResults"][0]["EvalActionName"]
            evDec = response["EvaluationResults"][0]["EvalDecision"]
            
            if evDec == "allowed":
                decisionEmoji = "\U00002705"
            else:
                decisionEmoji = "\U0000274c"

            print("{} - {} on {}".format(decisionEmoji, evAction,evResource))

    def simulateCaps(self, config, role):
        
        responseList = []

        for action in config["actions"]:  
            for resource in config["resources"]:
                response = self.iam_client.simulate_principal_policy(
                    PolicySourceArn = role,
                    ActionNames = [action],
                    ResourceArns = [resource]
                )
            
            responseList.append(response)
            
        
        self.generateOutput(responseList)