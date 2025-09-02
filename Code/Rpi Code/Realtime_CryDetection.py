import os
from pathlib import Path
import math, random
import torch
import torchaudio
from torchaudio import transforms
from IPython.display import Audio
#import matplotlib.pyplot as plt
from sklearn.tree import DecisionTreeClassifier
import random
from tqdm import tqdm
from sklearn.neural_network import MLPClassifier
import pickle
import time
import paho.mqtt.client as mqtt



from gpiozero import OutputDevice




broker = "test.mosquitto.org"
port = 1883  
topic = "home/sensor"  
client_id = "RaspberryPi" 


def on_connect(client, userdata, flags, rc):
    print(f"Connected to MQTT broker with result code: {rc}")
   
    publish_data(client)


def publish_data(client,data):
    
    
    client.publish(topic, data)
    print(f"Published data: {data}")
    

client = mqtt.Client(client_id)
client.on_connect = on_connect


client.connect(broker, port, 60)


























IN1 = OutputDevice(14)
IN2 = OutputDevice(15)
IN3 = OutputDevice(18)
IN4 = OutputDevice(23)
number_of_revolutions=4

step_sequence = [  [1,0,0,0],
                   [1,1,0,0],
                   [0,1,0,0],
                   [0,1,1,0],
                   [0,0,1,0],
                   [0,0,1,1],
                   [0,0,0,1],
                   [1,0,0,1], ]

def set_step(w1,w2,w3,w4):
	IN1.value = w1
	IN2.value = w2
	IN3.value = w3
	IN4.value = w4

def step_motor(steps,direction=1,delay=0.001):
	for _ in range(steps):
		for step in (step_sequence if direction > 0 else reversed(step_sequence)):
			set_step(*step)
			time.sleep(delay)


def spin_the_motor():
    print("Spinning")
    x=0
    global number_of_revolutions
    while x<number_of_revolutions:
        step_motor(250,1)
        step_motor(250,-1)
        x=x+1
       
	
	







def pad_list(lst, length):
    print("Here1")
    lst.extend([0] * (length - len(lst)))
    return lst

def open_audio_file(audio_file):
    print("HERE2")
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
    print("HERE3")
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
    print("HERE4")
    ''' Return a list containing two lists'''
    cd=os.getcwd()
    data_folder=os.path.join(cd,'Actual_Dataset','Train_Audio')
    obj=os.scandir(data_folder)
    true_files=[]
    false_files=[]
    print("Scanning Dataset")
    time.sleep(0.02)
    for i in tqdm(obj,total=772):
        time.sleep(0.1)
        filename=str(i)[11:-2]
        if filename[0] == 'T':
            true_files.append(os.path.join(str(data_folder),filename))
        elif filename[0] == 'F' :
            false_files.append(os.path.join(str(data_folder),filename))

    
    return get_features(true_files,false_files)

    


def stereo_to_mono(open_audio_file_signal):
    print("HERE5")
    if open_audio_file_signal.shape[0] > 1:
        return torch.mean(open_audio_file_signal,dim=0,keepdim=True)
    

def resample(signal,sample_rate,new_sample_rate=40000):
    print("HERE6")
     
    if(sample_rate == new_sample_rate):
        return (signal,sample_rate)
    
    new_signal=torchaudio.transforms.Resample(sample_rate,new_sample_rate)(signal[:1,:])

    

    return (new_signal,new_sample_rate)
    






for i in range(4):
    os.system('arecord -D plughw:2,0 -c 2 -d 10 -f cd test.wav')
    this_directory=os.getcwd()
    model_file=os.path.join(this_directory,"Trained_Model_DT2.sav")
    loaded_model=pickle.load(open(model_file,'rb'))
    baby_crying = loaded_model.predict(open_audio_file("test.wav")[0])
    print(baby_crying)
    publish_data(client,baby_crying[0])
    if(baby_crying[0]=='T'):
        print("Entered here")
        x=6
        spin_the_motor()
    os.remove("test.wav")
    print("Sleeping")
    time.sleep(10)














#this_directory=os.getcwd()
#model_file=os.path.join(this_directory,)
#print("here")
#loaded_model=pickle.load(open(model_file,'rb'))
#print("done")


