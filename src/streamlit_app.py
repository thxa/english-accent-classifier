import streamlit as st
import os
from transformers import pipeline
from transformers.utils import logging
import numpy as np 
import pandas as pd
import yt_dlp
import torchaudio
import ffmpeg

logging.set_verbosity_info()

RATE_HZ = 16000
MAX_SECONDS = 1
MAX_LENGTH = RATE_HZ * MAX_SECONDS
MAX_SEGMENTS = 250

def download_video(url, output_path="video.mp4"):
    ydl_opts = {
        'format': 'worstvideo[ext=mp4]+bestaudio[ext=m4a]/bestaudio',
        'outtmpl': output_path,
        'merge_output_format': 'mp4',
        'quiet': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'retries': 3,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return output_path

def extract_audio(input_path, output_path="audio.mp3"):
    (
        ffmpeg
        .input(input_path)
        .output(output_path, format='mp3', acodec='libmp3lame', audio_bitrate='192k')
        .overwrite_output()
        .run(quiet=True)
    )
    return output_path

def split_audio(file):
    segmented_audio = []
    try:
        audio, rate = torchaudio.load(str(file))
        transform = torchaudio.transforms.Resample(rate, RATE_HZ)
        num_segments = (len(audio[0]) // MAX_LENGTH)  # Floor division to get segments
        for i in range(num_segments):
            if i >= MAX_SEGMENTS:
                break
            start = i * MAX_LENGTH
            end = min((i + 1) * MAX_LENGTH, len(audio[0]))
            segment = audio[0][start:end]
            segment = transform(segment).squeeze(0).numpy().reshape(-1)
            segmented_audio.append(segment)
    except Exception as e:
        print(f"Error processing file: {e}")
        return segmented_audio
    else:
        return np.concatenate(segmented_audio)

accent_mapping = {
    'us': 'American',
    'canada': 'Canadian',
    'england': 'British',
    'indian': 'Indian',
    'australia': 'Australian',
}

st.set_page_config(page_title="Accent Classifier", layout="centered")
st.title("🎙️ English Accent Classifier")
st.markdown("Upload a video link and get the English accent with confidence.")
video_url = st.text_input("Paste a public video URL (Loom, or MP4):")

if st.button("Analyze"):
    if not video_url.strip():
        st.warning("Please enter a valid URL.")
    else:
        with st.spinner("Downloading video..."):
            video_path = download_video(video_url)

        with st.spinner("Extracting audio..."):
            audio_path = extract_audio(video_path)

        with st.spinner("Extracting Waves..."):
            waves = split_audio(audio_path)

        with st.spinner("Classifying accent..."):
            model_name = "dima806/english_accents_classification"
            pipe = pipeline('audio-classification', model=model_name, device=0)
            # accent_data = accent_classify(pipe, audio_path)
            accent_data = pipe(waves)[0]
            accent = accent_mapping.get(accent_data.get("label", "us"))
            confidence = accent_data.get("score", 0)

        st.success("Analysis Complete!")
        st.markdown(f"**Accent:** {accent}")
        st.markdown(f"**Confidence Score:** {confidence:.2f}%")

        # Cleanup
        os.remove(video_path)
        os.remove(audio_path)
