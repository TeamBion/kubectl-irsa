import boto3

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
        
        for resource in config["resources"]:

            response = self.iam_client.simulate_principal_policy(
                PolicySourceArn = role,
                ActionNames = config["actions"],
                ResourceArns = [resource]
            )
            
            responseList.append(response)
        
        self.generateOutput(responseList)