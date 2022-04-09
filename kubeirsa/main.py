from kubeirsa.iam import IAMPolicySimulator
from kubeirsa.config import Config
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
        "--role",
        action='store',
        type=str,
        help="IAM role name",
        required=True)

    return parser.parse_args()

def main():
    args = argParser()
    configObj = Config()
    iamObj = IAMPolicySimulator()

    configFile = args.config
    role = args.role
    configData = configObj.parseConfig(configFile)
    configDataCheck = configObj.configCheck(configData)

    if configDataCheck == True:
        iamObj.simulateCaps(config=configData, role=role)
    else:
        logging.error("Check the configuration please :))")
        sys.exit(1)