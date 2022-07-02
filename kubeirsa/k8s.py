from kubernetes import client, config
import sys
import logging

class Kubernetes(object):
    def __init__(self):
        config.load_kube_config()
        self.v1 = client.CoreV1Api()
        self.admissionClient = client.AdmissionregistrationV1Api()
    
    def checkAdmissionWebhook(self):
        
        try :
            result = self.admissionClient.read_mutating_webhook_configuration(name="pod-identity-webhook")
            decisionEmoji = "\U00002705"
            print("Pod identity webhook is existing in there {}".format(decisionEmoji))
        except client.exceptions.ApiException as exp:
            decisionEmoji = "\U0000274c"
            print("Resource not found {}".format(decisionEmoji))
        except Exception as defaultExp:
            print(defaultExp)

    def parseSA(self, name="default", namespace="default"):
        result = self.v1.read_namespaced_service_account(name=name, namespace=namespace)
        
        try:
            parsedSa = result.to_dict()
            roleName = parsedSa["metadata"]["annotations"]["eks.amazonaws.com/role-arn"]
            

        except Exception as exp:
            logging.error("""There is an error while parsing serviceaccount error is;
                        {}
                        """.format(exp))
            sys.exit(1)

        return roleName