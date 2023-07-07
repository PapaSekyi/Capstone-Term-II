import string
import re
from nltk import sent_tokenize
import nltk
import pint
ureg = pint.UnitRegistry()
# IN the is we get all the symbols associated with the data 
import pickle 
import numpy as np
import numpy as np
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.models import Sequential,load_model
from tensorflow.keras.layers import Dense,LSTM,Activation
from tensorflow.keras.optimizers import RMSprop
from goose3 import Goose
stopwords=nltk.corpus.stopwords.words('english')




# def predict_next_word(words):
#     return words

def get_data():
    while True: 
        url1 =f'https://en.wikipedia.org/wiki/{genre1}'
        try:
            text=Goose().extract(url1).cleaned_text
            print("Got Data Successfully")
            return text 
        except:
            print(" Failed To get Data")


def preprocess_data():
    text=get_data()
    text=text.replace('\n','')
    text=text.lower() 
    text=sent_tokenize(text)
    save_text = text 
    translator = str.maketrans('','',string.punctuation + '0123456789'+'•°'+'─')
    clean_text=[]
    for i in text:
        a=i.translate(translator)
        clean_text.append(a) 
    cleaner_text=[]
    for i in clean_text:
        l=[]
        for j in i.split():
            if j not in stopwords+list(ureg):
                l.append(j)
        cleaner_text.append(' '.join(l)) 
    text = ' '.join(cleaner_text)    
    tokens=text.split()
    print(f"Total data that we are taking in consideration is {len(tokens)}\n") 
    print(f" Unique words in our data is {len(set(tokens))}\n")
    # Need to save the tokenizer here 
    length = 4
    lines=[]
    for i in range(length,len(tokens)):
        seq=tokens[i-length:i]
        line = ' '.join(seq)
        lines.append(line)
    predicted_word=[] 
    for i in range(len(tokens)-4):
        predicted_word.append(tokens[i+4])
    tokenizer=Tokenizer()
    tokenizer.fit_on_texts(lines)
    sequences= np.array(tokenizer.texts_to_sequences(lines))
    output_sequences=tokenizer.texts_to_sequences(predicted_word)
    X = np.zeros((len(sequences)-2,4,len(set(tokens))),dtype='bool')
    y= np.zeros((len(output_sequences)-2,len(set(tokens))),dtype='bool')
    sequences=sequences[:len(sequences)-10]
    output_sequences=output_sequences[:len(output_sequences)-10]
    for i,words in enumerate(sequences):# Here basically i gives you the index and the words are a set of 1st column that we see.
    # to the J we are only passing 4 word sequnece, 
        for j,word in enumerate(words):
        # there are going to be 1309 j values
            X[i,j,word] =1  # just giving value of 1 to each word that we have
        y[i,output_sequences[i][0]]=1
# SO here basically we have mapped out each word in an array of 750 words to have a value of 1.
# Save the tokenizer to a file using pickle
    with open(f'tokenizer_{genre1}.pickle', 'wb') as f:
        pickle.dump(tokenizer, f)
    print('preprocessing_successfull')
    global size
    size=len(set(tokens))
    print(size) 
    return X,y

def run_model(X,y,size):
    model = Sequential()
    model.add(LSTM(128,input_shape=(4,size),return_sequences=True))
    model.add(LSTM(128))
    model.add(Dense(size))
    model.add(Activation('softmax'))
    model.compile(loss='categorical_crossentropy',optimizer=RMSprop(learning_rate=0.01),metrics=['accuracy'])
    model.fit(X,y,batch_size=128,epochs=40,shuffle=True) 
    print('Saving Model')
    model.save(f"{genre1}.h5") 

def predict_next_word(input_text,genre,size):# best n predictions 
    genre1=genre
    size=size 
    m=[]
    with open(f'tokenizer_{genre1}.pickle', 'rb') as f: 
        tokenizer = pickle.load(f) 
        print('tokenizer loaded') 
    model = load_model(f"{genre1}.h5")
    n={value: key for key, value in tokenizer.word_index.items()}
    input_text=' '.join(input_text)
    print(input_text) 
    input_text=input_text.lower() 
    input_sequence=tokenizer.texts_to_sequences([input_text])[0]
    X=np.zeros((1,4,size))  # 1 set with 4 words each in a vector representation of 750 words
    # we only have set of one array
    for i,word in enumerate(input_sequence):
        X[0,i,word]=1
    predict=model.predict(X)[0]
    print("The best possible 4 words are: -\n") 
    for i in np.argsort(predict)[-4:][::-1]:
        print(n[i])
        m.append(n[i])
    return m 


def train_model(genre):
    global genre1
    genre1=genre
    X,y=preprocess_data()
    try:
        model = load_model(f"{genre1}.h5") 
        return size 
    except:
        run_model(X,y,size)
    return size  
