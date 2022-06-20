from kubeirsa.eks import EKS
from kubeirsa.iam import IAMPolicySimulator IAM
from kubeirsa.config import Config
from kubeirsa.serviceaccount import Kubernetes

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
    iamObj = IAMPolicySimulator()
    eksObj = EKS()
    k8s = Kubernetes()

    configFile = args.config
    sa = args.sa
    namespace = args.namespace

    configData = configObj.parseConfig(configFile)
    configDataCheck = configObj.configCheck(configData)

    roleName = k8s.parseSA(name=sa, namespace=namespace)

    if configDataCheck == True:
        iamObj.simulateCaps(config=configData, role=roleName)
        iamObj.checkOIDC(config=configData)
    else:
        logging.error("Check the configuration please :))")
        sys.exit(1)
