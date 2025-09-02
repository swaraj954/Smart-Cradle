import os
from pathlib import Path
import math, random
import torch
import torchaudio
from torchaudio import transforms
from IPython.display import Audio
import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
import random
from tqdm import tqdm
from sklearn.neural_network import MLPClassifier
import pickle
import time

def pad_list(lst, length):
    lst.extend([0] * (length - len(lst)))
    return lst

def open_audio_file(audio_file):
    #print(audio_file)
    class_id= audio_file.split('\\')[-1][0]
    #print(class_id)
    signal, sample_rate = torchaudio.load(audio_file)
    
    signal=stereo_to_mono(signal)

   # print(sample_rate)
   # print("------------------------")
    signal, sample_rate=resample(signal,sample_rate)
    #print(sample_rate)
    #print('__________________________________________________________________')
    
    #print(signal)
    #spectogram=generate_spectogram((signal,sample_rate))
    #return (spectogram,class_id)

    return (signal,class_id)


def get_features(true_files,false_files):

    ''' Returns a list of features and a list of labels '''
    audio_objects=[]
    Junk_Files=[]
    print("Loading Dataset(first half)")
    time.sleep(0.2)
    for i in tqdm(range(len(false_files))):
        try:
            temp=open_audio_file(false_files[i])
            audio_objects.append(temp)
        except Exception:
            #print("Junk File:"+ str(false_files[i]))
            Junk_Files.append(str(false_files[i]))

    print("Loading Dataset(second half)")
    time.sleep(0.2)
    for i in tqdm(range(len(true_files))):

        try:
            temp=open_audio_file(true_files[i])
            audio_objects.append(temp)
        except Exception:
            #print("Junk File:"+ str(true_files[i]))
            Junk_Files.append(str(true_files[i]))
    print("-----------------------------------------------")      
    print("Could not load the following files because they may be corrupt:")
    for x in Junk_Files:
        print(x)

    print("Count of invalid files:"+str(len(Junk_Files)))
    print("------------------------------------------------------")
    random.shuffle(audio_objects)

    features=[]
    labels=[]
    print("Extracting Features:")
    for i in tqdm(range(len(audio_objects))):
        x=audio_objects[i][0][0].tolist()
        if not(len(x)==400000):
            pad_list(x,400000)
        features.append(x)
        labels.append(audio_objects[i][1])

    
    return [features,labels]
    



        

    

        
    
    
    

def get_file_paths():
    ''' Return a list containing two lists'''
    cd=os.getcwd()
    data_folder=os.path.join(cd,'Actual_Dataset','Train_Audio')
    obj=os.scandir(data_folder)
    true_files=[]
    false_files=[]
    print("Scanning Dataset")
    time.sleep(0.2)
    for i in tqdm(obj,total=772):
        time.sleep(0.01)
        filename=str(i)[11:-2]
        if filename[0] == 'T':
            true_files.append(os.path.join(str(data_folder),filename))
        elif filename[0] == 'F' :
            false_files.append(os.path.join(str(data_folder),filename))

    
    return get_features(true_files,false_files)

    


def stereo_to_mono(open_audio_file_signal):
    if open_audio_file_signal.shape[0] > 1:
        return torch.mean(open_audio_file_signal,dim=0,keepdim=True)
    

def resample(signal,sample_rate,new_sample_rate=40000):

    if(sample_rate == new_sample_rate):
        return (signal,sample_rate)
    
    new_signal=torchaudio.transforms.Resample(sample_rate,new_sample_rate)(signal[:1,:])

    

    return (new_signal,new_sample_rate)
    

def generate_spectogram(open_audio_file,n_mels=64, n_fft=1024, hop_len=None):
    signal=open_audio_file[0]
    sample_rate=open_audio_file[1]
    top_db = 80
    spectogram = transforms.MelSpectrogram(sample_rate, n_fft=n_fft, hop_length=hop_len, n_mels=n_mels)(signal)

    spectogram = transforms.AmplitudeToDB(top_db=top_db)(spectogram)

    
    return (spectogram)
    


#model=MLPClassifier(verbose=True)
model = DecisionTreeClassifier(max_depth=20)
x=get_file_paths()
print("Training model:")

model.fit(x[0],x[1])

pickle.dump(model,open(os.path.join(os.getcwd(),"Trained_Model_DT.sav"),'wb'))
print("DONE")




