from flask import Flask, request, make_response
from werkzeug.utils import secure_filename
from speech_to_text import get_text
import json
import intent_classifier
import process_intent

app = Flask(__name__)

# load intent classification model
classifier = intent_classifier.classifier()


# load ner model

@app.route('/', methods=['GET', 'POST'])
def hello():
    return json.dumps({"data": "hello world"})


@app.route('/ner', methods=['GET'])
def ner():
    print(request.args["data"])
    return json.dumps({'data': "asd"})


@app.route('/upload', methods=['POST'])
def upload_file():
    f = request.files['file']
    f.save(secure_filename('output.flac'))
    text = get_text('output.flac')  # get text from the sound file
    intent = classifier.predict(text)
    process_intent.process(text, intent)
    return json.dumps({"data": text})


@app.route('/home', methods=['GET'])
def SayHello():
    return json.dumps({"data": "Hello World"})


app.run(host='0.0.0.0')
