import requests
import sys
import argparse

def testEndpoint(endpointURL, requestMethod, expectedStatus, expectedResponse):
    print("Testing endpoint: '{}' with method {}".format(endpointURL, requestMethod))
    response = requests.request(requestMethod, url=endpointURL)
    if response.status_code in expectedStatus and (response.text == expectedResponse or expectedResponse == None):
        print("Test PASSED\n")
        return 0
    print("Test FAILED")
    print("Expected status:{}\nRecieved status:{}".format(expectedStatus, response.status_code))
    print("Expected response:{}\nRecieved response:{}".format(expectedResponse, response.text))
    global failedCount
    failedCount = failedCount + 1
    return 1

def testEndpointJSON(url, method, requestData, expectedStatus, expectedResponse):
    return 0

failedCount = 0


parser = argparse.ArgumentParser()
parser.add_argument('--host', dest='HOSTNAME', default='localhost', help='Specify the hostname for the API (default: localhost)')
parser.add_argument('--port', dest='PORT', default='5000', help='Specify the port on the API host (default: 5000)')
args = parser.parse_args()


hostname = args.HOSTNAME
port = args.PORT

apiURL = 'http://{}:{}'.format(hostname, port)


try:
    request = requests.get(apiURL)
except:
    print("Error contacting API, please ensure that hostname and port are correct.")
    sys.exit(1)


testEndpoint(apiURL + "/md5", 'GET', [400,404,405], None)
testEndpoint(apiURL + "/md5/test", 'GET', [200], "098f6bcd4621d373cade4e832627b4f6")
testEndpoint(apiURL + "/md5/hello%20world", 'GET', [200], "5eb63bbbe01eeed093cb22bb8f5acdc3")
    ('/slack-alert/test',         'GET',  [200], True),
    ('/slack-alert/'+HTTP_ENCODE, 'GET',  [200], True),
