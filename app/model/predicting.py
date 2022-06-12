def predict(text, model):
    logits = model.predict([text])
    label = logits.predictions.argmax(1)[0]

    return label
