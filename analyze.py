from birdnetlib import Recording
from birdnetlib.analyzer import Analyzer
from datetime import datetime
from pydub import AudioSegment
import os
import pandas as pd

base_dir = "./"
sounds = os.listdir(os.path.join(base_dir,"sounds"))

sounds_df_list = []

# Load and initialize the BirdNET-Analyzer models.
analyzer = Analyzer()

for sound in sounds:

    sound_name = sound.split('.')[0]

    src_path = os.path.join(base_dir,"sounds",sound)
    dest_path = os.path.join(base_dir,f"{sound_name}.mp3")
    AudioSegment.from_wav(src_path).export(dest_path, format="mp3")

    recording = Recording(
        analyzer,
        f"{sound_name}.mp3",
        lat=35.4244,
        lon=-120.7463,
        date=datetime(year=2022, month=5, day=10), # use date or week_48
        min_conf=0.25,
    )
    recording.analyze()

    sound_df = pd.DataFrame(recording.detections)
    sound_df["file"] = sound_name

    sounds_df_list.append(sound_df)

    os.remove(dest_path)

sounds_df = pd.concat(sounds_df_list)
sound_df.to_csv("./birds_analyzed.csv",index=False)