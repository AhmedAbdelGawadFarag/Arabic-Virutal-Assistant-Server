import tensorflow as tf
from tensorflow import keras
from transformers import BertTokenizer, TFBertModel


class classifier:
    def __init__(self):
        model_path = "intent-model"
        self.MAX_LENGHT = 32
        self.classes = ['call contact', 'search', 'alarm', 'weather']

        self.model = keras.models.load_model(model_path, custom_objects={"TFBertModel": TFBertModel})
        self.tokenizer = BertTokenizer.from_pretrained("aubmindlab/bert-base-arabertv02-twitter")

    def predict(self, text):
        ids = self.tokenizer(text, return_tensors="tf", padding='max_length', max_length=self.MAX_LENGHT)['input_ids']
        result = self.model.predict(ids)
        return self.classes[tf.math.argmax(result[0])]
