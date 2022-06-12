from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
import os

import pandas as pd
import re

factory = StemmerFactory()
stemmer = factory.create_stemmer()

factory = StopWordRemoverFactory()
stopword = factory.create_stop_word_remover()

kata_baku = pd.read_csv(f'{os.path.join(os.path.dirname(__file__))}/kamus_baku.csv')
kata_baku = kata_baku.set_index("kataAlay")["kataBaik"].to_dict()

def cleansing(text):
    text = str(text)

    # Mengubah setiap kata menjadi lowercase
    text = text.lower()

    # Menghapus Link Dengan Pattern http/https dan www
    text = re.sub(r'http\S+', '', text)
    text = re.sub('(@\w+|#\w+)', '', text)

    # Menghapus Tag HTML
    text = re.sub('<.*?>', '', text)

    # Menghapus Karakter Selain Huruf a-z dan A-Z
    text = re.sub('[^a-zA-Z]', ' ', text)

    # Mengganti baris baru (enter) dengan spasi
    text = re.sub("\n", " ", text)

    # Menghapus Spasi Yang Lebih Dari Satu
    text = re.sub('(s{2,})', ' ', text)

    # Menghapus kata yang mengandung judul topik dan kata yang terdapat pada stopwords indonesia
    temp_text_split=[]
    final_text=[]
    text_split=text.split(' ')

    # Menghapus kata yang mengandung judul topik dan kata yang terdapat pada stopwords indonesia
    temp_text_split = []
    final_text = []
    text_split = text.split(' ')

    # Merubah kata baku dan filter kata harus >= 2
    for i in range(len(text_split)):
        if text_split[i] != 'ptn':
            if text_split[i] in kata_baku and text_split[i] != 'telkom':
                text_split[i] = kata_baku[text_split[i]]

            if len(list(str(text_split[i]))) >= 2:
                temp_text_split.append(str(text_split[i]))

    for i in range(len(temp_text_split)):
        if temp_text_split not in final_text:
            final_text.append(str(temp_text_split[i]))

    text = ' '.join(final_text)
    text = stopword.remove(text)
    text = stemmer.stem(text)

    # Mengembalikan Hasil Preprocessing Text
    return text
