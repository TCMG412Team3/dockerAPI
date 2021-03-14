from flask import Flask
app = Flask(__name__)

@app.route('/md5/<md5Input>')
def md5(md5Input):
    return "md5"

@app.route('/factorial/<factorialInput>')
def factorial(factorialInput):
    return "factorial"

@app.route('/fibonacci/<fibInput>')
def fibonacci(fibInput):
    return "fibonacci"

@app.route('/is-prime/<primeInput>')
def prime(primeInput):
    return "prime"

@app.route('/slack-alert/<slackInpute>')
def slack(slackInpute):
    return "slack"


if __name__== '__main__':
    app.run()
