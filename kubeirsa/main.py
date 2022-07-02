from kubeirsa.iam import IAMPolicySimulator, IAM
from kubeirsa.config import Config
from kubeirsa.k8s import Kubernetes

import argparse
import logging
import sys

def argParser():
    parser = argparse.ArgumentParser(description="kubectl irsa configurations")

    parser.add_argument(
        "--config",
        action='store',
        type=str,
        help="the path of the configuration file",
        default="config.yaml")

    parser.add_argument(
        "--sa",
        action='store',
        type=str,
        help="IAM role name",
        required=True)

    parser.add_argument(
        "--namespace",
        action='store',
        type=str,
        help="IAM role name",
        default="default")

    return parser.parse_args()

def main():
    args = argParser()
    configObj = Config()
    iamPolicyObj = IAMPolicySimulator()
    iamObj = IAM()
    k8s = Kubernetes()

    configFile = args.config
    sa = args.sa
    namespace = args.namespace

    configData = configObj.parseConfig(configFile)
    configDataCheck = configObj.configCheck(configData)

    roleName = k8s.parseSA(name=sa, namespace=namespace)

    if configDataCheck == True:
        iamPolicyObj.simulateCaps(config=configData, role=roleName)
        iamObj.checkOIDC(config=configData)
        roleStr = roleName.split(':', 5)
        roleStr = roleStr[5].replace("role/", "")
        iamObj.checkTrustPolicy(roleName = roleStr)
        k8s.checkAdmissionWebhook()
    else:
        logging.error("Check the configuration please :))")
        sys.exit(1)
