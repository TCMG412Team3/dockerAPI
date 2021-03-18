from flask import Flask
import os
import requests
import json

webhook_url = os.getenv('WEBHOOK_URL')

app = Flask(__name__)

#md5
import hashlib
@app.route('/md5/<md5Input>')
def md5(md5Input):
    md5Output = hashlib.md5(md5Input.encode())
    output = {"input":md5Input, "output": md5Output.hexdigest()}
    return json.dumps(output)

@app.route('/factorial/<factorialInput>')
def factorial(factorialInput):
    return "factorial"

@app.route('/fibonacci/<fibInput>')
def fibonacci(fibInput):
    fibInput = int(fibInput)
    if fibInput < 0:
        output = {"input":fibInput, "output":"Error. Input is not positive."}
        return json.dumps(output)
    if fibInput == 0:
        output = {"input":fibInput, "output":[0]}
        return json.dumps(output)
    if fibInput == 1:
        output = {"input":fibInput, "output":[1]}
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
    return "prime"

@app.route('/slack-alert/<slackInput>')
def slack(slackInput):
    postData = {'text': slackInput}
    response = requests.post(webhook_url, data=json.dumps(postData), headers={'Content-Type': 'application/json'})
    if response.status_code != 200:
        output = {"input":slackInput, "output":"False"}
        return json.dumps(output)
    else:
        output = {"input":slackInput, "output":"True"}
        return json.dumps(output)


if __name__== '__main__':
    app.run()
