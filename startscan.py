#!/usr/bin/python
import sys, getopt
from smartcheck import *
import json


class CreateScanException(Exception):
    def __init__(self, response):
        super(CreateScanException, self).__init__('scan', response)


smart_check_url = ''
smart_check_userid = ''
smart_check_password = ''
scan_registry = ''
scan_repository = ''
scan_tag = 'latest'
aws_region = 'us-east-2'
aws_id = ''
aws_secret = ''
scan_name = 'Python Script Scan'
scan_id = 'v1'
scan_aws = "no"
registry_user = ""
registry_password = ""

def init(argv):
    try:
        opts, args = getopt.getopt(argv, "h:v", ["smart_check_url=", "smart_check_userid=", "smart_check_password=",
                                                 "scan_registry=", "scan_repository=", "scan_tag=", "aws_region=",
                                                 "aws_id=", "aws_secret=", "scan_id=", "scan_aws=", "registry_user=", "registry_password="])

    except getopt.GetoptError as error:
        print('Error Not enough Arguments')
        print(str(error))
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('scans.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ("--smart_check_url"):
            global smart_check_url
            smart_check_url = arg

        elif opt in ("--smart_check_userid"):
            global smart_check_userid
            smart_check_userid = arg

        elif opt in ("--smart_check_password"):
            global smart_check_password
            smart_check_password = arg

        elif opt in ("--scan_registry"):
            global scan_registry
            scan_registry = arg

        elif opt in ("--scan_repository"):
            global scan_repository
            scan_repository = arg

        elif opt in ("--scan_tag"):
            global scan_tag
            scan_tag = arg

        elif opt in ("--scan_aws"):
            global scan_aws
            scan_aws = arg

        elif opt in ("--aws_region"):
            global aws_region
            aws_region = arg

        elif opt in ("--aws_id"):
            global aws_id
            aws_id = arg

        elif opt in ("--aws_secret"):
            global aws_secret
            aws_secret = arg

        elif opt in ("--registry_user"):
            global registry_user
            registry_user = arg

        elif opt in ("--registry_password"):
            global registry_password
            registry_password = arg

        elif opt in ("--scan_name"):
            global scan_name
            scan_name = arg

        elif opt in ("--scan_id"):
            global scan_id
            scan_id = arg



init(sys.argv[1:])


def get_token(userid, password):
    # print("----- Generating Token ----- "+userid)
    payload = {'user': {'userID': userid, 'password': password}}
    r = requests.post('https://' + smart_check_url + '/api/sessions', json=payload, verify=False)
    # print(r)
    z = json.loads(r.text)
    # print(z['token'])
    return z


def credentials(scan_aws):
    payload = {}

    if scan_id:
        # print("scan ID Not Empty ")
        payload['id'] = scan_id
    payload['id'] = scan_id
    payload['name'] = scan_name
    payload['source'] = {}
    payload['source']['type'] = "docker"
    payload['source']['registry'] = scan_registry
    payload['source']['repository'] = scan_repository
    payload['source']['tag'] = scan_tag
    if scan_aws == "yes":
        payload['source']['credentials'] = {}
        payload['source']['credentials']['aws'] = {}
        payload['source']['credentials']['aws']['region'] = aws_region
        payload['source']['credentials']['aws']['accessKeyID'] = aws_id
        payload['source']['credentials']['aws']['secretAccessKey'] = aws_secret
    else:
        payload['source']['credentials'] = {}
        payload['source']['credentials']['username'] = registry_user
        payload['source']['credentials']['password'] = registry_password


    return payload


access = credentials(scan_aws)
token = get_token(smart_check_userid, smart_check_password)
url = smart_check_url
obj = Smartcheck(smart_check_url, smart_check_userid, smart_check_password)
print("json data", credentials(scan_aws))
result = obj.create_scan(token['token'], smart_check_url, access)
print("result", result)
