import requests
import sys
import argparse

def testEndpoint(endpointURL, requestMethod, expectedStatus, expectedResponse):
    print("Testing endpoint: '{}' with method {}".format(endpointURL, requestMethod))
    response = requests.request(requestMethod, url=endpointURL)
    if response.status_code in expectedStatus and (expectedResponse == None or response.json()["output"] == expectedResponse):
        print("Test PASSED\n")
        return 0
    print("Test FAILED")
    print("Expected status:{}\nRecieved status:{}".format(expectedStatus, response.status_code))
    print("Expected response:{}\nRecieved response:{}".format(expectedResponse, response.text))
    global failedCount
    failedCount = failedCount + 1
    return 1

def testEndpointJSON(endpointURL, requestMethod, requestData, expectedStatus, expectedResponse):
    print("Testing endpoint: '{}' with method {}".format(endpointURL, requestMethod))
    response = requests.request(requestMethod, url=endpointURL, json=requestData)
    if response.status_code in expectedStatus and (expectedResponse == None or response.json() == expectedResponse):
        print("Test PASSED\n")
        return 0
    print("Test FAILED")
    print("Expected status:{}\nRecieved status:{}".format(expectedStatus, response.status_code))
    print("Expected response:{}\nRecieved response:{}".format(expectedResponse, response.text))
    global failedCount
    failedCount = failedCount + 1
    return 1

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



#TESTS

testEndpoint(apiURL + "/md5", 'GET', [400,404,405], None)
testEndpoint(apiURL + "/md5/test", 'GET', [200], "098f6bcd4621d373cade4e832627b4f6")
testEndpoint(apiURL + "/md5/hello%20world", 'GET', [200], "5eb63bbbe01eeed093cb22bb8f5acdc3")
testEndpoint(apiURL + "/factorial/3",'GET',[200],6)
testEndpoint(apiURL + "/factorial/4",'GET',[200],24)
testEndpoint(apiURL + "/factorial/6",'GET',[200],720)
testEndpoint(apiURL + "/is-prime/1", 'GET', [200], False)
testEndpoint(apiURL + "/is-prime/2", 'GET', [200], True)
testEndpoint(apiURL + "/is-prime/5", 'GET', [200], True)
testEndpoint(apiURL + "/is-prime/6", 'GET', [200], False)
testEndpoint(apiURL + "/is-prime/37", 'GET', [200], True)

testEndpointJSON(apiURL+"/keyval/test", 'GET', "", [404], {"key":"test", "value":"", "command": "GET test", "result": False, "error": "Unable to retrieve pair: key does not exist."})
testEndpointJSON(apiURL+"/keyval", 'POST', {"key":"test", "value":"testval"}, [200], {"key":"test", "value":"testval", "command": "SET test testval NX", "result": True, "error": ""})
testEndpointJSON(apiURL+"/keyval/test", 'GET', "", [200], {"key":"test", "value":"testval", "command": "GET test", "result": True, "error": ""})
testEndpointJSON(apiURL+"/keyval", 'POST', {"key":"test", "value":"testval"}, [409], {"key":"test", "value":"testval", "command": "SET test testval NX", "result": False, "error": "Unable to add pair: key already exists."})


