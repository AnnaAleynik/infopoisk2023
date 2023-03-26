import nltk
import math
import os
import sys
import json
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download('punkt')
nltk.download("stopwords")
nltk.download('wordnet')

# получаем список стоп слов
stop = stopwords.words('english')
stop_ru = stopwords.words('russian')

# соберем все леммы 
lemmas = []
f = open('../task2/lemmas.txt', encoding='utf-8')
data = f.read()
lines = data.splitlines()
for line in lines:
  lemmas.append(line.split(':')[0])

# print(lemmas)

# создадим файл с векторами (вот тут не понятно токены использовать или леммы)
for dirpath, _, filenames in os.walk('../task4'):
  for filename in filenames:
    if "lemmas" not in filename:
      continue
    dictionary = {}
    vector = {}
    file = open('../task4/' + filename, encoding='utf-8')
    data = file.read()
    lines = data.splitlines()

    for line in lines:
      word = line.split(' ')[0]
      idf = line.split(' ')[1]
      dictionary[word] = idf


    for lemma in lemmas:
      if lemma in dictionary.keys():
        vector[lemma] = dictionary[lemma]
      else: 
        vector[lemma] = 0

    with open('../task5/vectors/' + filename, 'w') as f:
      for key, idf_val in vector.items():
        f.write(f"{key} ")
        f.write(f"{idf_val} ")  
        f.write(f"\n") 

def convert_file_to_vector(filename):
    vector_dict = {}
    file = open('../task5/vectors/' + filename, encoding='utf-8')
    vecotor_strings = file.read().splitlines()
    file.close()
    for vecotor_string in vecotor_strings:
        if vecotor_string != "":
            vector_dict[vecotor_string.split(" ")[0]] = float(vecotor_string.split(" ")[1])
    return vector_dict

def vector_length(vector):
    return math.sqrt(sum(x ** 2 for x in vector.values()))

def compare_vectors(v1, v2):
    len = 0
    len_v1 = vector_length(v1)
    len_v2 = vector_length(v2)
    for lemma in lemmas:
        len = len + v1[lemma] * v2[lemma]
  
    if (len == 0 or len_v1 == 0 or len_v2 == 0):
      return 0

    return len / (math.sqrt(len_v1) * math.sqrt(len_v2))

def search(search_term):
    current_lemmas = set()
    search_dictionary = {}
    vector_dict = {}

    # file = open("../tokens")
    # tokens = file.read().split("\n")
    # file.close()

    for lemma in lemmas:
        search_dictionary[lemma] = 0

    # убираем стоп слова из поисковой строки
    search_term = '  '.join([word for word in search_term.split() if word not in (stop_ru)])
    words = search_term.split()

    # считаем вектор для поисковой строки 
    for word in words:
        current_lemma = WordNetLemmatizer().lemmatize(word)
        current_lemmas.add(current_lemma)
        if word not in search_dictionary.keys():
            search_dictionary[word] = 0
        search_dictionary[word] = search_dictionary[word] + 1

    for lemma in lemmas:
        vector_dict[lemma] = 0
        
    for lemma in current_lemmas:
        vector_dict[lemma] = search_dictionary[lemma] / float(len(words))

    result_dict = {}
    for dirpath, _, filenames in os.walk('../task5/vectors'):
      for filename in filenames:
        res = compare_vectors(convert_file_to_vector(filename), vector_dict)
        result_dict[filename] = res
    return result_dict

result = sorted(search(sys.argv[1]).items(), key=lambda item: item[1], reverse=True)
# print(result)
sys.stdout.write(json.dumps(result))