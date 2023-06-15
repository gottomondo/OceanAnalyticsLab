#!/usr/bin/env python

import os
import glob
import shutil
import sys
import json
import requests

#Get auth info from env variables
refreshtoken = os.environ["ccprefreshtoken"]
context = os.environ["ccpcontext"]
clientid = os.environ["ccpclientid"]
iam = os.environ["ccpiamurl"]

#Auth related functions
logindata = { 'grant_type' : 'refresh_token', 'client_id' : clientid, 'refresh_token' : refreshtoken}
loginheaders = { "Accept" : "application/json", "Content-Type" : "application/x-www-form-urlencoded"}

umadata = { 'grant_type' : 'urn:ietf:params:oauth:grant-type:uma-ticket', 'audience' : context}
umaheaders = { "Accept" : "application/json", "Content-Type" : "application/x-www-form-urlencoded"}

def getToken():
    # login with offline_token
    resp1 = requests.post(iam, data=logindata, headers=loginheaders)
    jwt = resp1.json()
    #get UMA token for context
    umaheaders["Authorization"] = "Bearer " + jwt["access_token"]
    resp2 = requests.post(iam, data=umadata, headers=umaheaders)
    return resp2.json()["access_token"]


# Example call to workspace: List VRE folder content
#vrefolder = requests.get(workspace-url + "/vrefolder", headers={"Accept" : "application/json", "Authorization" : "Bearer " + tok}).json()

def main():
    f = open("/ccp_data/parameters.txt", "r")
    print("parameters are")
    print(f.read())
    print("A new token")
    print(getToken())


if __name__ == '__main__':
    main()
