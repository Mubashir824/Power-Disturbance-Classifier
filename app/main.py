from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import shutil
import os
from scipy.io import wavfile
import numpy as np
import tensorflow as tf

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

UPLOAD_DIR = "user_file"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def root():
    return FileResponse("static/index.html")

last_uploaded_file = None  # Store uploaded path


import matplotlib.pyplot as plt

@app.post("/upload_wave")
async def upload_wave(file: UploadFile = File(...)):
    global last_uploaded_file
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    last_uploaded_file = file_path

    # Read audio data
    sample_rate, data = wavfile.read(file_path)
    data = data.astype(np.float32)

    # Convert to mono if stereo
    if data.ndim > 1:
        data = data[:, 0]

    # Compute time axis for the full data
    duration = len(data) / sample_rate
    time = np.linspace(0., duration, len(data))

    # Only plot a reduced number of points (e.g., 5000 evenly spaced points)
    max_points = 5000
    if len(data) > max_points:
        indices = np.linspace(0, len(data) - 1, max_points, dtype=int)
        data_plot = data[indices]
        time_plot = time[indices]
    else:
        data_plot = data
        time_plot = time

    # Plot waveform
    plt.figure(figsize=(10, 4))
    plt.plot(time_plot, data_plot)
    plt.title("Waveform")
    plt.xlabel("Time [s]")
    plt.ylabel("Amplitude")
    plt.tight_layout()

    # Save plot as image
    plot_path = os.path.join("static", "waveform.png")
    plt.savefig(plot_path)
    plt.close()

    return {"filename": file.filename, "waveform_plot": "/static/waveform.png"}


@app.get("/predict")
async def predict():
    if not last_uploaded_file:
        return {"error": "No file uploaded"}

    model = tf.keras.models.load_model("cnn_model.keras")
    sample_rate, data = wavfile.read(last_uploaded_file)
    data = data.astype(np.float32)

    # Normalize between -1 and 1 if necessary (depends on your recording scale)
    data = data / np.max(np.abs(data))

    # Define chunk size
    chunk_size = 128

    # Trim the data to make it divisible by chunk size
    num_chunks = len(data) // chunk_size
    data_trimmed = data[:num_chunks * chunk_size]

    # Reshape into (num_chunks, 128)
    X = data_trimmed.reshape(num_chunks, chunk_size)
    pred=model.predict(X.reshape(X.shape[0], X.shape[1], 1))
    pred_class = np.argmax(pred)
    class_mapping = {
        0: "Normal",
        1: "Harmonic wave",
        2: "3rd harmonic wave",
        3: "5th harmonic wave",
        4: "Voltage dip",
        5: "Transient"
    }
    print(pred_class)
    pred_class = class_mapping.get(pred_class, "Unknown")
    print(pred_class)
    return {"prediction": pred_class}
