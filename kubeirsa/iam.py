import boto3
from eks import EKS

class IAM(object):

    def __init__(self):
        self.iam_client = boto3.client("iam")
        self.oidcId = None
        sts_client = boto3.client("sts")
        
        self.accountId = sts_client.get_caller_identity()["Account"]

    def checkTrustPolicy(self, roleName):
        data = self.iam_client.get_role(RoleName= roleName)
        
        statements = data["Role"]["AssumeRolePolicyDocument"]
        federatedUrl = "arn:aws:iam::{}:oidc-provider/{}".format(self.accountId, self.oidcId)
        print(federatedUrl)

        for statement in statements["Statement"]:
            try:            
                if statement["Principal"]["Federated"] == federatedUrl:
                    decisionEmoji = "\U00002705"
                    print("The OIDC configuration is looking fine {}".format(decisionEmoji))
                else:
                    decisionEmoji = "\U0000274c"
                    print("Check role principals {}".format(decisionEmoji))
            except KeyError as exp:
                decisionEmoji = "\U0000274c"
                print("Missing {} data that returned from aws missing key {} :: {}".format(type(exp).__name__, exp, decisionEmoji))
            except Exception as exp:
                print("Another error occured")

    def checkOIDC(self, config):
        clusterName = config["clusterName"]

        eksObj = EKS()

        oidcId = eksObj.oidcIssuerId(clusterName)
        self.oidcId = oidcId
        openIdProviders = self.iam_client.list_open_id_connect_providers()
        
        for openIdProvider in openIdProviders["OpenIDConnectProviderList"]:
            if openIdProvider["Arn"] == "arn:aws:iam::{}:oidc-provider/{}".format(self.accountId, oidcId):
                providerArn = openIdProvider["Arn"]
                status = 1
                break
            else:
                status = 0


        if status == 1:
            print()
            decisionEmoji = "\U00002705"
            print("OIDC provider connectivity between IAM and EKS is :: {}".format(decisionEmoji ))
            oidcDetails = self.iam_client.get_open_id_connect_provider(OpenIDConnectProviderArn=providerArn)

            if oidcDetails["ClientIDList"][0] == "sts.amazonaws.com":
                decisionEmoji = "\U00002705"
                print("The audience configuration looks fine {}".format(decisionEmoji))
            else:
                decisionEmoji = "\U0000274c"
                print("Please check audience configuration and set it as sts.amazonaws.com {}".format(decisionEmoji))

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


obj = IAM()
obj.checkOIDC({"clusterName": "test-cluster"})
obj.checkTrustPolicy("ack-s3-controller")