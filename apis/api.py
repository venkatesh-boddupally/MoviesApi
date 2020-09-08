from flask import Flask


app = Flask(__name__)

@app.route('/')
def hello():
    return 'hello'

app.run(port=5004, debug=True)
