# 🎙️ English Accent Classifier

This is a **Streamlit web application** that classifies **English accents** from public video URLs (e.g., Loom, mp4). It uses Hugging Face model and a full audio preprocessing pipeline built on `yt-dlp`, `ffmpeg`, and `torchaudio`.

---

## 🧠 Features

- 🧩 **Downloads video** from a public URL
- 🎵 **Extracts and processes audio**
- 🧠 **Classifies the speaker's English accent**
- ✅ Displays **accent and confidence score**
<!-- - (Optional) Transcribes speech using OpenAI Whisper -->

---

## 🌍 Supported Accents

| Label     | Displayed Accent |
|-----------|------------------|
| `us`      | American         |
| `canada`  | Canadian         |
| `england` | British          |
| `indian`  | Indian           |
| `australia` | Australian     |

---

## 🚀 Try It Out
> ⚠️ **Note:** The app may take approximately **30 seconds** to classify the accent, depending on audio length and server load.
### 1. Copy this sample video URL:
```plaintext
https://www.loom.com/share/002508e86fde4232bb8de474eb5c65c4?sid=62a90dca-4600-491a-aa35-1ed119580294
```
```plaintext
https://www.bbc.com/news/videos/cdxvlr0gqw0o
```

### 2. Open the demo app on Hugging Face Spaces:
https://huggingface.co/spaces/7H4M3R/Audio

### 3. Paste the URL into the app to classify the accent.


## 🐳 Run with Docker (Locally)

### 1. Clone the repository

```bash
git clone https://github.com/thxa/english-accent-classifier.git
cd english-accent-classifier
```

### 2. Build the Docker image
```bash
docker build -t english-accent-classifier .
```

### 3. Run the Docker container
```bash
docker run -p 8501:8501 english-accent-classifier 
```


### 4. Open the app
Visit http://localhost:8501 in your browser.




