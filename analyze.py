from birdnetlib import Recording
from birdnetlib.analyzer import Analyzer
from datetime import datetime
from pydub import AudioSegment
import os
import pandas as pd
import re

base_dir = "./"
sounds = [file for file in os.listdir(os.path.join(base_dir,"sounds")) if not file == ".DS_Store"]

sounds_df_list = []

# Load and initialize the BirdNET-Analyzer models.
analyzer = Analyzer()

for sound in sounds:

    sound_name = sound.replace(".wav","")

    src_path = os.path.join(base_dir,"sounds",sound)
    dest_path = os.path.join(base_dir,f"{sound_name}.mp3")
    wav = AudioSegment.from_wav(src_path)
    wav.export(dest_path, format="mp3")

    coords = re.search(".*_(-?\\d+\\.\\d+)_(-?\\d+\\.\\d+)$",sound_name)
    lon = float(coords.group(1))
    lat = float(coords.group(2))

    recording = Recording(
        analyzer,
        f"{sound_name}.mp3",
        lat=lat,
        lon=lon,
        date=datetime(year=2022, month=5, day=10), # use date or week_48
        min_conf=0.25,
    )
    recording.analyze()

    sound_df = pd.DataFrame(recording.detections)
    sound_df["file"] = sound_name
    sound_df["group_index"] = list(range(sound_df.shape[0]))

    sounds_df_list.append(sound_df)

    for row_index in range(sound_df.shape[0]):
        row = sound_df.iloc[row_index,:]
        start_second = 1000 * row["start_time"]
        end_second = 1000 * row["end_time"]
        wav_cut = wav[start_second:end_second]
        dest_cut_path = os.path.join(base_dir,"sounds_cut",f"{row['group_index']}_{row['file']}.mp3")
        wav_cut.export(dest_cut_path,format="mp3")

    os.remove(dest_path)

sounds_df = pd.concat(sounds_df_list)
sounds_df["correct"] = None
sounds_df["suggestion"] = None
sounds_df.to_csv("./birds_analyzed.csv",index=False)
