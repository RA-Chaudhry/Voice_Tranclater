# 🎙️ Voice Translator (FastAPI + Groq + Gemini + Edge TTS)

This project is a powerful voice translator web application built using **FastAPI** backend and **React** frontend. It allows users to:
- Upload an audio file and get a transcription using **Groq Whisper AI**
- Translate the transcribed text into **100+ languages** using **Gemini**
- Convert translated text into speech using **Edge TTS**
- Download the translated audio file (WAV)

---

## 📂 Project Structure

```

Voice\_Tranclater/
├── .env                       # Environment variables (API keys)
├── .gitignore                 # Git ignore file
├── README.md                  # Project documentation
├── app.py                     # FastAPI backend application
├── index.html                 # Fallback page (for testing)
├── pyproject.toml             # Python project dependencies
├── requirements.txt           # Python dependencies list
├── speech\_edgetts.wav         # Output speech file (auto-generated)
├── static/
│   └── images/                # Images used in frontend
│       ├── \*.png / \*.jpg
├── uv.lock                    # Poetry or pipenv lock file (if used)
└── frontend/                  # React frontend (optional structure)
├── src/
├── public/
└── ...

````

---

## 🚀 Features

✅ Upload audio  
✅ Transcribe speech with **Groq Whisper**  
✅ Translate to multiple languages using **Gemini AI**  
✅ Text-to-speech with natural voice using **Edge TTS**  
✅ WAV audio download  
✅ Multi-language support (Urdu, English, Hindi, French, etc.)  

---

## 🔧 Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/RA-Chaudhry/Voice_Tranclater.git
cd Voice_Tranclater
````

### 2. Create and activate virtual environment (optional but recommended)

```bash
python -m venv venv
venv\Scripts\activate     # On Windows
source venv/bin/activate  # On Linux/macOS
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create `.env` file

Create a `.env` file in the root directory and add:

```
GROQ_API_KEY=your_groq_api_key
GEMINI_API_KEY=your_gemini_api_key
```

---

## ▶️ Run the FastAPI Server

```bash
uvicorn app:app --reload
```

Then open [http://localhost:8000](http://localhost:8000) in your browser.

---

## 🌍 Deployment

You can deploy the app using platforms like:

* **Render**
* **Replit**
* **PythonAnywhere**
* **Railway**
* **VPS (with Nginx + Uvicorn)**

---

## 🧠 Tech Stack

| Tech      | Usage                            |
| --------- | -------------------------------- |
| Python    | Backend logic                    |
| FastAPI   | API creation                     |
| Groq      | Audio transcription (Whisper V3) |
| Gemini AI | Text translation                 |
| Edge TTS  | Text-to-speech conversion        |
| React JS  | Frontend user interface          |

---

## 📌 TODO / Future Enhancements

* [ ] Add user login system (optional)
* [ ] Store past translations for history
* [ ] Support real-time microphone recording
* [ ] Host frontend and backend online

---

## 🤝 Contributing

Contributions are welcome! Please fork the repo and submit a pull request.

---

## 📄 License

This project is licensed under the MIT License.

---

## ✨ Acknowledgements

* [Groq Whisper](https://console.groq.com/)
* [Google Gemini](https://ai.google.dev/)
* [Edge TTS](https://github.com/rany2/edge-tts)
* [FastAPI](https://fastapi.tiangolo.com/)
