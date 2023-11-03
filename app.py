import streamlit as st
import os 
import pandas as pd
import numpy as np

#common_name,scientific_name,start_time,end_time,confidence,label,file,group_index,correct,suggestion

src_path = "./"
sounds = os.listdir(os.path.join("sounds_cut"))
sounds_df = pd.read_csv("./birds_analyzed.csv")

if "df" in st.session_state:
    sounds_df = st.session_state.df

st.set_page_config(layout="wide")
st.title("Fabis Birds")

st.write("")
if st.button("Save to File",type="primary"):
    sounds_df.to_csv("./birds_analyzed.csv",index=False)
    st.info("Successfully saved!")

st.header("Audios",divider="red")
st.write("")
st.write("")

for row_index in range(sounds_df.shape[0]):
    row = sounds_df.iloc[row_index,:]
    audio_file = open(os.path.join(src_path,"sounds_cut",f"{row['group_index']}_{row['file']}.mp3"), 'rb')
    audio_bytes = audio_file.read()

    filename_col, audio_col, bird_col, confirm_col ,result_col,suggestion_col = st.columns([0.15,0.25,0.2,0.15,0.1,0.15])

    with filename_col:
        st.markdown(f"<p style='text-align: center;'><i>{row['file']}.wav ({row['start_time']}-{row['end_time']} seconds)</i></p>",unsafe_allow_html=True)
        st.write(f"confidence score: :red[{round(row['confidence'],2)}]")
    with audio_col:
        st.audio(audio_bytes, format='audio/wav',start_time=3)
    with bird_col:
        if type(sounds_df.loc[row_index,"suggestion"])!=str:
            st.markdown(f"<p style='text-align: center;'><b>{row['common_name']}</b> (<i>{row['scientific_name']}</i>)</p>",unsafe_allow_html=True)
        else:
            st.markdown(f"<s style='text-align: center;'><b>{row['common_name']}</b> (<i>{row['scientific_name']}</i>)</s>",unsafe_allow_html=True)
            st.markdown(f"<i>alternative: </i><b>{sounds_df.loc[row_index,'suggestion']}</b>",unsafe_allow_html=True)


    with confirm_col:

        yes_col, no_col = st.columns(2)

        with yes_col:
            if st.button("True",key=f"{row['group_index']}_{row['file']}_yes"):
                sounds_df.loc[row_index,"correct"] = True
                sounds_df.loc[row_index,"suggestion"] = None
                st.session_state["df"] = sounds_df
                st.rerun()
        with no_col:
            show_text = False
            st.session_state["show_text"] = show_text
            if st.button("False",key=f"{row['group_index']}_{row['file']}_no",type="primary"):
                sounds_df.loc[row_index,"correct"] = False
                sounds_df.loc[row_index,"suggestion"] = None
                st.session_state["df"] = sounds_df
                show_text = True
                st.session_state["show_text"] = show_text

    with suggestion_col:
            disabled=(not st.session_state.show_text)
            suggestion = st.text_input("Alternative bird",key=f"{row['group_index']}_{row['file']}_no_suggestion",disabled=disabled)
            if st.button("Confirm",key=f"{row['group_index']}_{row['file']}_no_suggestion_confirm"):
                if suggestion != "":
                    sounds_df.loc[row_index,"suggestion"] = suggestion
                    st.session_state["df"] = sounds_df
                    st.rerun()
                else:
                    sounds_df.loc[row_index,"suggestion"] = None
                    st.session_state["df"] = sounds_df
                    st.rerun()




    with result_col:
        if not np.isnan(sounds_df.loc[row_index,"correct"]):
            if sounds_df.loc[row_index,"correct"]:
                st.write(":bird:")
            else:
                st.write(":x: :bird:")
        else:
            st.markdown("*No decision yet...*")

    st.divider()


