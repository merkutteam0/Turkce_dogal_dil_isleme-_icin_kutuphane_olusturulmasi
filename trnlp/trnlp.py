# -*- coding: utf-8 -*-
"""
Created on Infinity

@author: team merkut
"""
from collections import Counter
import numpy as np
import string 
import pandas as pd
import joblib


"""
dağılım analizi
"""

class dagilim(Counter):
    def __init__(self, ornek=None):
        return Counter.__init__(self, ornek)


"""
duraklar
"""


def duraklar():
    try:
        d = open("turkce-duraklar.txt", "r",encoding="utf8")
    except:
        raise Exception("Failed to find turkce-duraklar.txt file")
    icerik = d.read()
    return set(icerik.split("\n"))

def silnktlm(liste):
    noktalama = list(string.punctuation)
    filtrelinktlm=[]
    for da in liste:
        if da not in noktalama:
            filtrelinktlm.append(da)
    return filtrelinktlm

def btnsilnktlm(liste):
    noktalama = list(string.punctuation)
    filtrelinktlm=[]
    for da in liste:
        sbt=0
        for nkt in noktalama:
            if nkt in da:
                sbt+=1
        if sbt==0:filtrelinktlm.append(da) 
    return filtrelinktlm



"""
simgeleştirme
"""

def simge(liste):
    islenmis=[];sonuc=[];hata="Argument type must be str or list of str";noktalama = list(string.punctuation )
    if type(liste)==str:liste=[liste]
    if type(liste)==list:
        for i in liste:
            if type(i)==str:
                for kr in noktalama:
                    if kr=="'":i=i.replace(kr," {}".format(kr))
                    else:i=i.replace(kr," {} ".format(kr))
                i=i.replace("I","ı");i=i.replace("İ","i")
                islenmis.append(i.lower())
            else: raise Exception(hata) 
    else: raise Exception(hata)
    for c in islenmis:
        son = (c.split(' '))
        son = list(filter(None, son))
        sonuc.extend(son)
    return sonuc



"""
Kök Ayır
"""


class kokAyir():
    def govdeAyir(self,liste):
        try:
            t = open("KOKLER.txt", "r",encoding="utf8")
        except:
                raise Exception("Failed to find KOKLER.txt file")
        tx = t.read()
        y=set(tx.split("\n"))
        y_ayrik=[]
        for ytum in y:
            y_ayrik.append(list(ytum.split(" ")))
        
        kelimeler=[]
        kokKelimeler=[]
        try:
            kelimelet= list(liste)
        except:
            raise Exception("Data must be iterable")
        for ke in kelimelet:
            kelimeler.append(ke.lower())
        """"""
        for ekgovde in kelimeler:
            koktemp=[]
            for kokler in y_ayrik:
                if ekgovde.startswith(kokler[0]):
                    koktemp.append(kokler[0])
            if len(koktemp)>=1: kokKelimeler.append(max(koktemp,key=len))
            elif len(koktemp)>=0: kokKelimeler.append(ekgovde)
        return kokKelimeler
    """ Stemmer"""
    def ektenAyir(self,liste,sinir=1,istisna=dict()):
        try:
            r = open("EKLER.txt", "r",encoding="utf8")
        except:
                raise Exception("Failed to find EKLER.txt file")
        rx = r.read()
        z=set(rx.split("\n"))
        z_ayrik=[]
        for ztum in z:
            z_ayrik.append(list(ztum.split(" ")))
        
        kelimeler=[]
        ekKelimeler=[]
        try:
            kelimelet= list(liste)
        except:
            raise Exception("Data must be iterable")
        for ke in kelimelet:
            kelimeler.append(ke.lower())
        """"""
        key_ = list(istisna.keys())
        val_ = list(istisna.values())
        for ekli in kelimeler:
            ektemp=[]
            for ekler in z_ayrik:
                if ekli.endswith(ekler[0]):
                    ektemp.append(ekler[0])
            sab=len(ekli)-len(max(ektemp,key=len))
            if ekli in list(istisna.keys()): pt = key_.index(ekli); ekKelimeler.append(val_[pt])
            elif sab<=sinir: ekKelimeler.append(ekli[0:sinir])
            elif len(ektemp)>=1: ekKelimeler.append(ekli.replace(max(ektemp,key=len),""))
            elif len(ektemp)>=0: ekKelimeler.append(ekli)
        return ekKelimeler    
    
"""
cumleAyir
"""

def cumleAyirici(paragraf):
    noktalama='.?!'
    paraf=[]
    ayrilmis=[]
    cumle=''
    try:
        paragraf=paragraf.lower()
        paraf.append(paragraf)
    except:
        raise Exception('Argument is not suitable for "cumleAyirici" function')
    try:
        for c in paraf:
            for i in range(len(c)):
                liste=[]
                if c[i] in noktalama:
                    cumle = cumle + c[i]
                    liste.append(cumle)
                    ayrilmis.append(liste)
                    cumle=''
                else: 
                    cumle = cumle + c[i]
    except:
        raise Exception('Argument is not suitable for "cumleAyirici" function')
    try:
        for ke in ayrilmis:
            for k in range(len(ke)):
                ke[k] = ke[k].strip()
            
    except:
        raise Exception('Argument is not suitable for "cumleAyirici" function')
    return ayrilmis



def cumleSilnktlm(cumleler):
    temizlenmis=[]
    cumlet=''
    try:
        for cumle in cumleler:
            for cum in cumle:
                liste=[]
                for cu in range(len(cum)):
                    if cum[cu] in string.punctuation:
                        pass
                    else:
                        cumlet= cumlet+ cum[cu]
            liste.append(cumlet)           
            temizlenmis.append(liste)
            cumlet=''
    except:
        raise Exception('Argument is not suitable for "cumlesilnktlm" function')
    return temizlenmis

    
def etiket(metin):
    df = pd.read_csv('postag.csv',index_col=(None),delimiter=",",header=0)
    sozluk=dict(df.values)
    kelimeler=[]
    etiketlenmis=[]
    try:
        kelimeles=list(metin)
    except:
        raise Exception('Argument is not suitable for "etiket" function')
    for k in kelimeles:
        kelimeler.append(k.lower())
    try:
        for ke in kelimeler:
            if ke in string.punctuation:
                tuplet=(ke , "NO")
            else:    
                tuplet=(ke , sozluk.get(ke))
            etiketlenmis.append(tuplet)
    except:
        raise Exception('Argument is not suitable for "etiket" function')
    return etiketlenmis

def ayiricietiketlenmis(paragraf):
    noktalama='.?!'
    ayrilmis=[]
    cumle=[]

    try:
        for c in paragraf:
            if c[0] in noktalama:
                cumle.append(c)
                ayrilmis.append(cumle)
                cumle=[]
            else: 
                cumle.append(c)
    except:
        raise Exception('Argument is not suitable for "ayiricietiketlenmis" function')
    return ayrilmis
"""" nitelikli etiketin içinde kullanmak için tanımlanmış fonksiyonlar"""
def features(sentence, index):
    """ sentence: [w1, w2, ...], index: the index of the word """
    return {
        'word': sentence[index],
        'is_first': index == 0,
        'is_last': index == len(sentence) - 1,
        'is_capitalized': sentence[index][0].upper() == sentence[index][0],
        'is_all_caps': sentence[index].upper() == sentence[index],
        'is_all_lower': sentence[index].lower() == sentence[index],
        'prefix-1': sentence[index][0],
        'prefix-2': sentence[index][:2],
        'prefix-3': sentence[index][:3],
        'suffix-1': sentence[index][-1],
        'suffix-2': sentence[index][-2:],
        'suffix-3': sentence[index][-3:],
        'prev_word': '' if index == 0 else sentence[index - 1],
        'next_word': '' if index == len(sentence) - 1 else sentence[index + 1],
        'has_hyphen': '-' in sentence[index],
        'is_numeric': sentence[index].isdigit(),
        'capitals_inside': sentence[index][1:].lower() != sentence[index][1:]
    }
 
def untag(tagged_sentence):
   return [w for w, t in tagged_sentence]


def transform_to_dataset(islenmis):
    X = []
    for tagged in islenmis:
        for index in range(len(tagged)):
            X.append(features(untag(tagged), index))
            
    return X

def tahmin(data):
    islenmis=[]
    islen=[]
    tuplem=()
    ayir=kokAyir()
    listem=ayir.govdeAyir(simge(data))
    tuplem=(listem[0],listem[0])
    islen.append(tuplem)
    islenmis.append(islen)
    model = joblib.load('model.pkl')
    X = transform_to_dataset(islenmis)
    ta = model.predict(X)
    tahmit = ta.tolist()
    return tahmit

"""nitekli etiket"""

def niteliklietiket(metin):
    df = pd.read_csv('postag.csv',index_col=(None),delimiter=",",header=0)
    sozluk=dict(df.values)
    kelimeler=[]
    etiketlenmis=[]
    try:
        kelimeles=list(metin)
    except:
        raise Exception('Argument is not suitable for "niteliklietiket" function')
    for k in kelimeles:
        kelimeler.append(k.lower())
    try:
        for ke in kelimeler:
            if not(ke in sozluk):
                tag=tahmin(ke)
                tuplet = (ke , tag[0])
            elif ke.isdigit():
                tuplet = (ke , 'SA')
            elif ke in string.punctuation:
                tuplet=(ke , ".")
            else:    
                tuplet=(ke , sozluk.get(ke))
            etiketlenmis.append(tuplet)
    except:
        raise Exception('Argument is not suitable for "niteliklietiket" function')
    return etiketlenmis
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

    

