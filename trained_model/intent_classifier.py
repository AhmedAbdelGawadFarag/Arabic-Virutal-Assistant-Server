import os

import tensorflow as tf
from tensorflow import keras
from transformers import BertTokenizer, TFBertModel
from colored_exception import logException


class classifier:
    def __init__(self):
        try:
            #model_path = "./trained_model/intent-model"
            #/home/ahmed/Desktop/ArabicIntentClassification/Arabic-Virutal-Assistant-Server/trained_model/intent-model
            model_path = os.getenv('intent_model_path')
            print("PAAAATH")
            print(model_path)
            self.MAX_LENGHT = 32
            self.classes = ['call contact', 'search', 'alarm', 'weather']

            self.model = keras.models.load_model(model_path, custom_objects={"TFBertModel": TFBertModel})
            self.tokenizer = BertTokenizer.from_pretrained("aubmindlab/bert-base-arabertv02-twitter")
        except Exception as e:
            logException(e)

    def predict(self, text):
        ids = self.tokenizer(text, return_tensors="tf", padding='max_length', max_length=self.MAX_LENGHT)['input_ids']
        result = self.model.predict(ids)
        return self.classes[tf.math.argmax(result[0])]
