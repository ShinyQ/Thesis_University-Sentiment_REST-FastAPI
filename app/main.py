from transformers import AutoModelForSequenceClassification, Trainer
from transformers import AutoTokenizer
from fastapi import FastAPI, Response
from pydantic import BaseModel
from typing import List

from .helper import api
from .model import preprocessing

import os

app = FastAPI(debug=True)

classifier = AutoModelForSequenceClassification.from_pretrained(f'{os.path.join(os.path.dirname(__file__))}/model/IndoBERT')
tokenizer = AutoTokenizer.from_pretrained("indobenchmark/indobert-base-p2")
model = Trainer(model=classifier)

class Input(BaseModel):
    text: str

@app.get('/', status_code=200)
def status(response: Response):
    return api.builder("IndoBERT University Sentiment API Works!", response.status_code)


@app.post("/predict", status_code=200)
def get_prediction(list: List[Input], response: Response):
    result = []

    for data in list:
        text = data.text
        preprocess = preprocessing.cleansing(text)
        tokenize = tokenizer(preprocess, padding='max_length', max_length=256)

        logits = model.predict([tokenize]).predictions
        predicted = logits.argmax(1)[0]
        logits = logits[0].tolist()

        result.append({
            "text": text,
            "preprocessing": preprocess,
            "probability": {
                "negative": logits[0],
                "neutral": logits[1],
                "positive": logits[2]
            },
            "label": str(predicted)
        })
    
    return api.builder(result, response.status_code)
