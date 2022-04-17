import flask
import requests
from flask import Flask, request, make_response
from werkzeug.utils import secure_filename
from asr.speech_to_text import get_text
import json
import trained_model.intent_classifier as intent_classifier
import trained_model.process_intent as process_intent
import base64
from pydub import AudioSegment

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
    print(request.get_json()['audio'])

    encode_string = request.get_json()['audio']
    wav_file = open("test.wav", "wb")
    decode_string = base64.b64decode(encode_string)
    wav_file.write(decode_string)

    song = AudioSegment.from_wav("test.wav")
    song.export("output.flac", format="flac")

    text = get_text('output.flac')  # get text from the sound file
    intent = classifier.predict(text)
    process_intent.process(text, intent)

    # print(request.files)

    text = get_text('output.flac')  # get text from the sound file
    print("yeeeeeeee")
    print(text)
    intent = classifier.predict(text)
    data = process_intent.process(text, intent)
    if intent == 'call contact':
        return json.dumps({'intent': intent, 'data': {"displayName": data}}), 200, {'ContentType': 'application/json'}
    elif intent == 'search':
        return json.dumps({'intent': intent, 'data': {"webSearchQuery": data}}), 200, {
            'ContentType': 'application/json'}


@app.route('/home', methods=['GET'])
def SayHello():
    return json.dumps({"data": "Hello World"})
