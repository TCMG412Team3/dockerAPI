from flask import Flask
from flask import request
import os
import requests
import json
import redis

webhook_url = os.getenv('WEBHOOK_URL')

app = Flask(__name__)
cache = redis.Redis(host='redis', port=6379)

#md5
import hashlib
@app.route('/md5/<md5Input>')
def md5(md5Input):
    md5Output = hashlib.md5(md5Input.encode())
    output = {"input":md5Input, "output": md5Output.hexdigest()}
    return json.dumps(output)

@app.route('/factorial/<factorialInput>')
def factorial(factorialInput):
    factorialInput = int(factorialInput)
    # checks if inputted number is negative
    if factorialInput <=0:
        output = {"input":factorialInput, "output": "Error: must enter a positive integer"}
        return json.dumps(output)
    # initializes factorial variable to 1
    factorial = 1
    # for every integer from 1 to inputted number
    for i in range(1, factorialInput + 1):
    # factorial = factorial *= 1
        factorial *= i
    # returns factorial
    output = {"input":factorialInput, "output": factorial}
    return json.dumps(output)

@app.route('/fibonacci/<fibInput>')
def fibonacci(fibInput):
    try:
        fibInput = int(fibInput)
    except:
        return "",400
    if fibInput < 0:
        output = {"input":fibInput, "output":"Error. Input is not positive."}
        return json.dumps(output)
    if fibInput == 0:
        output = {"input":fibInput, "output":[0]}
        return json.dumps(output)
    if fibInput == 1:
        output = {"input":fibInput, "output":[0,1,1]}
        return json.dumps(output)
    numbers = [0, 1]
    while numbers[len(numbers)-1] < fibInput:
        if not numbers[len(numbers)-1] + numbers[len(numbers)-2] <= fibInput:
            break
        numbers.append(numbers[len(numbers)-1] + numbers[len(numbers)-2])
    output = {"input":fibInput, "output":numbers}
    return json.dumps(output)

@app.route('/is-prime/<primeInput>')
def prime(primeInput):
    # is-prime program

    num = int(primeInput)
    if num == 1:
        output = {"input":primeInput, "output": False}
        return json.dumps(output)
    if num > 1:
        for i in range (2, int(num/2)+1):
            if (num % i) == 0:
                output = {"input":primeInput, "output": False}
                return json.dumps(output)
        else:
            output = {"input":primeInput, "output": True}
            return json.dumps(output)
    output = {"input":primeInput, "output": "Error. Input is not greater than 0"}
    return json.dumps(output)

@app.route('/slack-alert/<slackInput>')
def slack(slackInput):
    postData = {'text': slackInput}
    response = requests.post(webhook_url, data=json.dumps(postData), headers={'Content-Type': 'application/json'})
    if response.status_code != 200:
        output = {"input":slackInput, "output":False}
        return json.dumps(output)
    else:
        output = {"input":slackInput, "output":True}
        return json.dumps(output)
    
    
    
@app.route('/keyval', methods=['POST'])
def keyvalPost():
    try:
        content = request.get_json()
        key = content['key']
        value = content['value']
    except:
        return "", 400
    command = "SET {} {} NX".format(key,value)
    if cache.set(key,value,nx=True) == True:
        output = {"key":key, "value":value, "command": command, "result": True, "error": ""}
        return json.dumps(output), 200
    else:
        output = {"key":key, "value":value, "command": command, "result": False, "error": "Unable to add pair: key already exists."}
        return json.dumps(output), 409
    

@app.route('/keyval/<keyGetInput>', methods=['GET'])
def keyvalGet(keyGetInput):
    command = "GET {}".format(keyGetInput)
    Value = cache.get(keyGetInput)
    if Value==None:
        output = {"key":keyGetInput, "value":"", "command": command, "result": False, "error": "Unable to retrieve pair: key does not exist."}
        return json.dumps(output), 404
    else:
        output = {"key":keyGetInput, "value":Value.decode("utf-8"), "command": command, "result": True, "error": ""}
        return json.dumps(output), 200
    

@app.route('/keyval', methods=['PUT'])
def keyvalPut():
    try:
        content = request.get_json()
        key = content['key']
        value = content['value']
    except:
        return "", 400
    command = "SET {} {} XX".format(key,value)
    if cache.set(key,value,xx=True) == True:
        output = {"key":key, "value":value, "command": command, "result": True, "error": ""}
        return json.dumps(output), 200
    else:
        output = {"key":key, "value":value, "command": command, "result": False, "error": "Unable to update value: Key does not exist."}
        return json.dumps(output), 404

@app.route('/keyval/<keyDeleteInput>', methods=['DELETE'])
def keyvalDelete(keyDeleteInput):
    command = "DEL {}".format(keyDeleteInput)
    if cache.delete(keyDeleteInput)==False:
        output = {"key":keyDeleteInput, "value":"", "command": command, "result": False, "error": "Unable to delete pair: key does not exist."}
        return json.dumps(output), 404
    else:
        output = {"key":keyDeleteInput, "value":"", "command": command, "result": True, "error": ""}
        return json.dumps(output), 200


if __name__== '__main__':
    app.run()
