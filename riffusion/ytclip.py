from pydub import AudioSegment
from pytube import YouTube
import librosa
import librosa.display
import matplotlib.pyplot as plt
import numpy as np
import gradio as gr
from io import BytesIO
from functools import partial
from PIL import Image

CLIP_FILENAME = "clip.wav"

spectro_from_wav = gr.Interface.load("spaces/fffiloni/audio-to-spectrogram")

# Define functions
def download_video(video_url):
    "Returns the path of the mp4 file downloaded from YouTube"
    yt = YouTube(video_url)
    video = yt.streams.filter(only_audio=True).first()
    out_file = video.download()
    return out_file


def load_audio(path=None, start_seconds=None, end_seconds=None):
    clip = AudioSegment.from_file(path)
    if end_seconds:
        clip = clip[: end_seconds * 1000]
    if start_seconds:
        clip = clip[start_seconds * 1000 :]
    return clip


def prepare_clip(path, start_seconds, num_beats, start_adj_ms, end_adj_ms, state):
    """
    Returns:
    - filepath
    - frame rate
    - tempo (BPM)
    - beat times (seconds)
    """
    # Trim the clip to 30 seconds
    if isinstance(path, tuple):
        path = path[0]
    clip = load_audio(path, start_seconds, start_seconds + 30)
    # Save to wav
    clip.export(CLIP_FILENAME, format="wav")
    # Load in librosa
    x, sr = librosa.load(CLIP_FILENAME, sr=clip.frame_rate)
    # Get the bpm and beats
    tempo, beats = librosa.beat.beat_track(y=x, sr=sr)
    beats = librosa.frames_to_time(beats, sr=sr) * 1000
    state["tempo"] = tempo
    state["beats"] = beats
    # Adjust the clip for number of beats and tolerance
    clip = load_audio(CLIP_FILENAME)
    clip = clip[beats[0] + start_adj_ms : beats[num_beats] + end_adj_ms]
    clip = clip.append(clip).append(clip).append(clip)
    clip.export(CLIP_FILENAME, format="wav")
    state["seconds"] = (
        (beats[num_beats] + end_adj_ms) - (beats[0] + start_adj_ms)
    ) / 1000.0
    state['duration_ms'] = (beats[num_beats] + end_adj_ms) - (beats[0] + start_adj_ms)
    return CLIP_FILENAME, clip.frame_rate, state


def get_clip_img():
    return Image.open(spectro_from_wav(CLIP_FILENAME)).convert("RGB")
