from flask import Flask, request, make_response
from asr.speech_to_text import get_text
import json
import base64
from pydub import AudioSegment
from werkzeug.utils import secure_filename
import requests
import os
from trained_model import intents


def getAudioFileFromRequest():
    if request.files.get('file') != None:

        f = request.files['file']
        f.save(secure_filename('output.flac'))
    elif request.get_json().get('audio') != None:

        encode_string = request.get_json()['audio']

        wav_file = open("test.wav", "wb")
        decode_string = base64.b64decode(encode_string)
        wav_file.write(decode_string)

        song = AudioSegment.from_wav("test.wav")
        song.export("output.flac", format="flac")


def handleUpload(classifier):
    print(request.files)

    if request.data.decode('utf-8') != '':  # request body has text not audio
        text = request.get_json()["text"]
        intent = classifier.predict(text)
        return handle_intent(intent, text)
    else:

        getAudioFileFromRequest()

        text = get_text('output.flac')  # get text from the sound file
        print(text)

        intent = classifier.predict(text)
        print(intent)

        return handle_intent(intent, text)


def handle_intent(intent, text):
    print("intent :" + intent)
    if intent == 'Call contact':
        return intents.call_contact(text)
    elif intent == 'New Calendar':
        return intents.new_calendar(text)
    elif intent == 'Read Calendar':
        return intents.read_calendar(text)
    elif intent == 'Search':
        return intents.search(text)
    elif intent == 'new contact':
        return intents.new_contact(text)
    elif intent == 'alarm':
        return intents.new_alarm(text)
    elif intent == 'Read notification':
        return intents.read_notifications()
    else:
        return json.dumps({'error': 'unknown intent'})
