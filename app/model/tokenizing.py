from transformers import AutoTokenizer

tokenizer = AutoTokenizer.from_pretrained("indobenchmark/indobert-base-p2")

def tokenize(text):
    return tokenizer(text, padding='max_length', max_length=256)
