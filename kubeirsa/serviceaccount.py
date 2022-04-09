from kubernetes import client, config
import sys
import logging

class Kubernetes(object):
    def __init__(self):
        config.load_kube_config()
        self.v1 = client.CoreV1Api()
    
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
