let uploaded = false;

function uploadFile() {
    const input = document.getElementById('fileInput');
    const file = input.files[0];
    if (!file) {
        alert("Please select a file first.");
        return;
    }

    const formData = new FormData();
    formData.append("file", file);

    fetch("http://127.0.0.1:8000/upload_wave", {
        method: "POST",
        body: formData,
    })
    .then(res => res.json())
    .then(data => {
        uploaded = true;
        document.getElementById("output").innerText = `Uploaded: ${data.filename}`;
    })
    .catch(err => console.error("Upload error:", err));
}

function getPrediction() {
    if (!uploaded) {
        alert("Please upload a file first.");
        return;
    }

    fetch("http://127.0.0.1:8000/predict")
    .then(res => res.json())
    .then(data => {
        document.getElementById("output").innerText = `Prediction: ${data.prediction}`;
    })
    .catch(err => console.error("Prediction error:", err));
}
