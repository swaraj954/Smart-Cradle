import yt_dlp as youtube_dl
import glob
import os
from pydub import AudioSegment
import pandas as pd
from pathlib import Path
from csv import reader
import time
from tqdm import tqdm

failed_downloads=0





def download_audio_from_youtube(link):
    ydl_opts= {
        'format': 'bestaudio/best',
        'quiet':True,
        'ignoreerrors':True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
            }],
        }
    
    with youtube_dl.YoutubeDL(ydl_opts) as downloader:
        downloader.download([link])
        

def get_recentmost_file():
    list_of_audio_files=glob.glob('./*.wav')
    return max(list_of_audio_files, key = os.path.getctime)
    


def timestamp_to_ms(timestamp):
    '''Converts each timestamp (H:M:S)y into a ms value'''
    segregate=timestamp.split(":")
    if (len(segregate)!=3):
        print("ERROR, INVALID TIMESTAMP")
        return 0
    
    return int(segregate[0])*60*60*1000+int(segregate[1])*60*1000+int(segregate[2])*1000

def trim_audio(wav_file,intial_timestamp,final_timestamp):
    untrimmed_audio=AudioSegment.from_file(wav_file)
    start=intial_timestamp
    finish=final_timestamp
    return untrimmed_audio[start:finish]


current_directory=Path(os.getcwd())
data_of_dataset_file=os.path.join(str(current_directory.parent.absolute().parent.absolute()),"Data_for_Dataset","data_of_train_data.csv")

def is_true_class(list_of_strings):
    for every_string in list_of_strings:
        
        if('/t/dd00002' in every_string):
            return True

    return False

class audio_object():
    def __init__(self,list_of_3,is_True):
        self.link=list_of_3[0]
        self.start_time=int(list_of_3[1])*1000
        self.finish_time=int(list_of_3[2])*1000
        self.label=is_True

    

def build_dataset():
    true_audio_object=[]
    false_audio_object=[]
    true_data=0
    false_data=0
    
    with open(data_of_dataset_file) as file_obj:
        csv_file=reader(file_obj)
        i=0
        limit=900
        
        skip=0
        progress_bar=tqdm(total=2*limit)
        print("Scanning Audioset File")
        for every_row in csv_file:
            
            i=i+1
            #print("Working on "+str(i)+"th row")
            
            if (every_row[0]=="#NAME?" or skip<=2):
                skip=skip+1
                continue
                
            else:
                if (is_true_class(every_row) and true_data<limit):
                    #print("ENTEREEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEED")
                    true_data=true_data+1
                    #print(true_data)
                    #time.sleep(1)
                    progress_bar.update(1)
                    true_audio_object.append(audio_object(every_row[0:3],True))       
                elif(false_data<limit):
                    false_data=false_data+1
                    false_audio_object.append(audio_object(every_row[0:3],False))
                    progress_bar.update(1)

            
            if(false_data>=limit and true_data>=limit):
                progress_bar.close()
                break

        print("Downloading Files:")
        for i in tqdm(range(limit)):
            #print("entered")
            extract_audio(true_audio_object[i])
            extract_audio(false_audio_object[i])
            
    
        
    
    print("Could not download "+str(failed_downloads)+" video(s) because they were either removed or made private")

    



def extract_audio(audioobj):
    yt_link="https://www.youtube.com/watch?v="+audioobj.link
    try:
        download_audio_from_youtube(yt_link)
        full_audio_file=get_recentmost_file()
        trimmed_audio=trim_audio(full_audio_file,audioobj.start_time,audioobj.finish_time)
        trimmed_audio.export("T_"+audioobj.link+".wav" if audioobj.label else "F_"+audioobj.link+".wav", format="wav")
        os.remove(full_audio_file)
    except Exception:
        global failed_downloads
        #print("Could not download:"+audioobj.link)
        failed_downloads=failed_downloads+1
                   
                    
                    
                    
                      
                               
        
    

build_dataset()


















                     
    

    


