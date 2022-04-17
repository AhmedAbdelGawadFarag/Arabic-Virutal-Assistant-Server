from flask import Flask, request, make_response
import json
import trained_model.intent_classifier as intent_classifier
from helpers import handleUpload, logException
import coloredlogs, logging

logger = logging.getLogger("logger")
coloredlogs.install(level='DEBUG', logger=logger)

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
        logException(logger, e)
        return json.dumps({"exception": str(e)})
