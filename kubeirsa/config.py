import sys
import yaml
import logging

class Config(object):

    def __init__(self):
        pass

    def parseConfig(self, configFile):

        with open(configFile, "r") as stream:
            try:
                content = yaml.safe_load(stream)
            except yaml.YAMLError as exp:
             logging.error(exp)

        return content

    def configCheck(self, content):

        configStatus = False

        if type(content["actions"]) is not list:
            logging.error("""
              actions should be string in yaml definition like this:
              actions: 
                - s3:GetObject
                - s3:PutObjectAcl
            """)

        else:
            configStatus = True
        
        return configStatus

