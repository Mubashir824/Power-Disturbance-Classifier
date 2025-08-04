
# Wave Classifier Dashboard

A user-friendly web dashboard for classifying current waveform `.wav` files into five categories using a trained machine learning model.

## Classes:
1. Harmonic wave  
2. 3rd harmonic wave  
3. 5th harmonic wave  
4. Voltage dip  
5. Transient

## Features:
- Upload `.wav` files via browser
- Visualize waveform plot
- Classify waveform into one of the five categories
- Achieves 97% accuracy on both training and test datasets

## Technologies Used:
- Python (Flask)
- TensorFlow / Keras
- SciPy, NumPy, Matplotlib
- HTML, CSS, JS

## How to Run

1. Clone this repository.
2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3. Run the Flask app:
    ```bash
    python app.py
    ```
4. Open your browser and go to `http://127.0.0.1:5000`.

## Folder Structure

```
wave_classifier_project/
├── app.py
├── static/
│   ├── style.css
│   ├── script.js
│   └── waveform.png (auto-generated)
├── templates/
│   └── index.html
├── model/
│   └── trained_model.h5
├── uploads/
│   └── your_uploaded_files.wav
├── README.md
└── requirements.txt
```

## Author
Mubashir Ali
