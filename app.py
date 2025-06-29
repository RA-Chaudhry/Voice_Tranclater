from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pathlib import Path
from tempfile import NamedTemporaryFile
from dotenv import load_dotenv
from groq import Groq
import google.generativeai as genai
import edge_tts
import shutil
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Language mapping for Edge TTS
LANGUAGE_TO_VOICE = {
    "Afrikaans": "af-ZA-AdriNeural",
    "Arabic": "ar-SA-ZariyahNeural",
    "Albanian": "sq-AL-AnilaNeural",
    "Amharic": "am-ET-AmehaNeural",
    "Armenian": "hy-AM-AnahitNeural",
    "Azerbaijani": "az-AZ-BabekNeural",
    "Bengali": "bn-BD-NabanitaNeural",
    "Bosnian": "bs-BA-VesnaNeural",
    "Bulgarian": "bg-BG-KalinaNeural",
    "Burmese": "my-MM-NilarNeural",
    "Catalan": "ca-ES-JoanaNeural",
    "Chinese": "zh-CN-XiaoxiaoNeural",
    "Croatian": "hr-HR-GabrijelaNeural",
    "Czech": "cs-CZ-VlastaNeural",
    "Danish": "da-DK-ChristelNeural",
    "Dutch": "nl-NL-ColetteNeural",
    "English": "en-US-JennyNeural",
    "Estonian": "et-EE-AnuNeural",
    "Filipino": "fil-PH-BlessicaNeural",
    "Finnish": "fi-FI-SelmaNeural",
    "French": "fr-FR-DeniseNeural",
    "Galician": "gl-ES-SabelaNeural",
    "Georgian": "ka-GE-EkaNeural",
    "German": "de-DE-KatjaNeural",
    "Greek": "el-GR-AthinaNeural",
    "Gujarati": "gu-IN-DhwaniNeural",
    "Hebrew": "he-IL-HilaNeural",
    "Hindi": "hi-IN-SwaraNeural",
    "Hungarian": "hu-HU-NoemiNeural",
    "Icelandic": "is-IS-GudrunNeural",
    "Indonesian": "id-ID-GadisNeural",
    "Irish": "ga-IE-OrlaNeural",
    "Italian": "it-IT-ElsaNeural",
    "Japanese": "ja-JP-NanamiNeural",
    "Javanese": "jv-ID-SitiNeural",
    "Kannada": "kn-IN-SapnaNeural",
    "Kazakh": "kk-KZ-AigulNeural",
    "Khmer": "km-KH-SreymomNeural",
    "Korean": "ko-KR-SunHiNeural",
    "Lao": "lo-LA-KeomanyNeural",
    "Latvian": "lv-LV-EveritaNeural",
    "Lithuanian": "lt-LT-OnaNeural",
    "Macedonian": "mk-MK-MarijaNeural",
    "Malay": "ms-MY-YasminNeural",
    "Malayalam": "ml-IN-SobhanaNeural",
    "Maltese": "mt-MT-GraceNeural",
    "Marathi": "mr-IN-AarohiNeural",
    "Mongolian": "mn-MN-YesuiNeural",
    "Nepali": "ne-NP-HemkalaNeural",
    "Norwegian": "nb-NO-IselinNeural",
    "Persian": "fa-IR-DilaraNeural",
    "Polish": "pl-PL-AgnieszkaNeural",
    "Portuguese": "pt-PT-RaquelNeural",
    "Punjabi": "pa-IN-GurpreetNeural",
    "Romanian": "ro-RO-AlinaNeural",
    "Russian": "ru-RU-SvetlanaNeural",
    "Serbian": "sr-RS-SophieNeural",
    "Sinhala": "si-LK-ThiliniNeural",
    "Slovak": "sk-SK-ViktoriaNeural",
    "Slovenian": "sl-SI-PetraNeural",
    "Spanish": "es-ES-ElviraNeural",
    "Swahili": "sw-KE-ZuriNeural",
    "Swedish": "sv-SE-SofieNeural",
    "Tamil": "ta-IN-PallaviNeural",
    "Telugu": "te-IN-ShrutiNeural",
    "Thai": "th-TH-PremwadeeNeural",
    "Turkish": "tr-TR-EmelNeural",
    "Ukrainian": "uk-UA-PolinaNeural",
    "Urdu": "ur-PK-UzmaNeural",
    "Uzbek": "uz-UZ-MadinaNeural",
    "Vietnamese": "vi-VN-HoaiMyNeural",
    "Welsh": "cy-GB-NiaNeural",
    "Zulu": "zu-ZA-ThandoNeural"
}

# Load environment variables from .env
load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GROQ_API_KEY or not GEMINI_API_KEY:
    logger.error("Missing API keys! Make sure GROQ_API_KEY and GEMINI_API_KEY are set in .env file")

# Initialize Groq client
groq_client = Groq(api_key=GROQ_API_KEY)

# Initialize Gemini client
genai.configure(api_key=GEMINI_API_KEY)
gemini_model = genai.GenerativeModel("gemini-2.0-flash")

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production to specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def read_root():
    try:
        return FileResponse('index.html')
    except Exception as e:
        logger.error(f"Error serving index.html: {str(e)}")
        raise HTTPException(status_code=500, detail="Error serving the frontend")

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        logger.info(f"Received audio file: {file.filename}")
        
        with NamedTemporaryFile(delete=False, suffix=file.filename) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        with open(tmp_path, "rb") as audio_file:
            transcription = groq_client.audio.transcriptions.create(
                file=(file.filename, audio_file.read()),
                model="whisper-large-v3",
                response_format="verbose_json",
            )

        os.remove(tmp_path)
        logger.info("Transcription completed successfully")
        return transcription.text
        
    except Exception as e:
        logger.error(f"Error in transcription: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

async def synthesize_with_edgetts(text: str, lang: str, output_path: str):
    try:
        voice = LANGUAGE_TO_VOICE.get(lang)
        if not voice:
            raise ValueError(f"Unsupported language: {lang}")
            
        communicate = edge_tts.Communicate(text=text, voice=voice)
        await communicate.save(output_path)
    except Exception as e:
        logger.error(f"Error in text-to-speech: {str(e)}")
        raise

@app.post("/translate-tts")
async def translate_and_tts(
    text: str = Form(...),
    target_language: str = Form(...)
):
    try:
        logger.info(f"Translating to {target_language}")
        
        if target_language not in LANGUAGE_TO_VOICE:
            raise HTTPException(status_code=400, detail=f"Unsupported language: {target_language}")
        
        # Translate the text using Gemini
        prompt = f"Translate to {target_language}: {text} \n\n Return only the translation. Do not include any other text not even something in brackets. Translation should be natural and fluent."
        response = gemini_model.generate_content(prompt)
        translated_text = response.text

        logger.info("Translation completed, starting text-to-speech")
        speech_file_path = Path("speech_edgetts.wav")
        await synthesize_with_edgetts(translated_text, target_language, str(speech_file_path))

        logger.info("Text-to-speech completed")
        return FileResponse(
            path=speech_file_path,
            media_type="audio/wav",
            filename="translated_speech.wav"
        )
        
    except Exception as e:
        logger.error(f"Error in translation/TTS: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
