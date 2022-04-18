import traceback

from flask import Flask, request, make_response
import json
import trained_model.intent_classifier as intent_classifier
from helpers import handleUpload
from colored_exception import logException

app = Flask(__name__)

# load intent classification model
classifier = intent_classifier.classifier()


@app.route('/', methods=['GET', 'POST'])
def hello():
    return json.dumps({"data": "hello world"})


@app.route('/upload', methods=['POST'])
def upload_file():
    try:
        return handleUpload(classifier)
    except Exception as e:
        logException(e)
        return json.dumps({"exception": str(e)})


@app.route('/home', methods=['GET'])
def sayHi():
    return json.dumps({"data": "hello world"})


@app.route('/intent_test', methods=['POST'])
def testIntent():
    return json.dumps({"data": classifier.predict('قم بالاتصال باحمد.')})


if __name__ == '__main__':
    print("YES")
    app.run(host='0.0.0.0', port=5000)
