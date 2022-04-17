from flask import Flask, request, make_response
from asr.speech_to_text import get_text
import json
import trained_model.process_intent as process_intent
import base64
from pydub import AudioSegment
from werkzeug.utils import secure_filename


def getAudioFileFromRequest():
    if request.files.get('file') != None:
        f = request.files['file']
        f.save(secure_filename('output.flac'))
    else:
        encode_string = request.get_json()['audio']

        wav_file = open("test.wav", "wb")
        decode_string = base64.b64decode(encode_string)
        wav_file.write(decode_string)

        song = AudioSegment.from_wav("test.wav")
        song.export("output.flac", format="flac")


def handleUpload(classifier):
    # encode_string = request.get_json()['audio']
    # wav_file = open("test.wav", "wb")
    # decode_string = base64.b64decode(encode_string)
    # wav_file.write(decode_string)

    # song = AudioSegment.from_wav("test.wav")
    # song.export("output.flac", format="flac")

    getAudioFileFromRequest()

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


def logException(logger, e):
    logger.critical("Exception: " + str(e))
