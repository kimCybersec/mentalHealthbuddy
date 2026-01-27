import google.generativeai as genai
import os
from api.utils.safetyChecker import is_safe

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPTS = {
    "en": "You are a compassionate mental health assistant focused on men's mental health but can also support women.",
    "sw": "Wewe ni msaidizi wa afya ya akili anayewasiliana kwa ufasaha kwa Kiswahili.",
    "fr": "Vous êtes un assistant en santé mentale qui communique couramment en français.",
    "es": "Eres un asistente de salud mental que se comunica con fluidez en español.",
    "de": "Sie sind ein psychischer Gesundheitsassistent, der fließend Deutsch spricht.",
    "it": "Sei un assistente di salute mentale che comunica fluentemente in italiano.",
    "pt": "Você é um assistente de saúde mental que se comunica fluentemente em português.",
    "zh": "您是一位流利使用中文的心理健康助手。",
    "ja": "あなたは日本語を流暢に話すメンタルヘルスアシスタントです。",
    "ar": "أنت مساعد الصحة النفسية الذي يتحدث العربية بطلاقة.",
    "hi": "आप एक मानसिक स्वास्थ्य सहायक हैं जो हिंदी में धाराप्रवाह बात करते हैं.",
    "ru": "Вы помощник по психическому здоровью, говорящий на русском языке.",
    "ko": "당신은 한국어를 유창하게 구사하는 정신 건강 도우미입니다.",
    "tr": "Sen Türkçe'yi akıcı bir şekilde konuşan bir zihinsel sağlık asistanısın.",
    "nl": "Je bent een geestelijke gezondheidsassistent die vloeiend Nederlands spreekt.",
    "no": "Du er en mental helseassistent som snakker flytende norsk.",
    "fi": "Olet mielenterveysavustaja, joka puhuu sujuvasti suomea.",
    "da": "Du er en mental sundhedsassistent, der taler flydende dansk.",
    "pl": "Jesteś asystentem zdrowia psychicznego, który płynnie mówi po polsku.",
    "cs": "Jste asistent duševního zdraví, který plynně mluví česky.",
    "el": "Είστε βοηθός ψυχικής υγείας που μιλάει άπταιστα ελληνικά.",
    "hu": "Ön egy mentális egészségügyi asszisztens, aki folyékonyan beszél magyarul.",
    "bg": "Вие сте асистент по психично здраве, който говори свободно български.",
    "ro": "Ești un asistent în sănătatea mintală care vorbește fluent română.",
    "vi": "Bạn là một trợ lý sức khỏe tâm thần nói tiếng Việt trôi chảy."
}


def generate_response(messages, lang="en"):
    if not messages:
        return {
            "reply": "How can I support you today?",
            "safety": False
        }

    last_msg = messages[-1].get("content", "")

    if not is_safe(last_msg):
        return {
            "reply": "If you are in immediate distress, please contact local mental health resources or emergency services.",
            "safety": True
        }

    system_prompt = SYSTEM_PROMPTS.get(lang, SYSTEM_PROMPTS["en"])

    gemini_messages = []

    # Inject system prompt into the first user message
    first = True
    for msg in messages:
        role = "user" if msg["role"] == "user" else "model"

        content = msg.get("content", "")

        if first and role == "user":
            content = f"{system_prompt}\n\n{content}"
            first = False

        gemini_messages.append({
            "role": role,
            "parts": [content]
        })

    model = genai.GenerativeModel("gemini-1.5-flash-latest")

    try:
        response = model.generate_content(
            gemini_messages,
            generation_config=genai.types.GenerationConfig(
                temperature=0.6,
                max_output_tokens=500
            )
        )

        return {
            "reply": response.text.strip(),
            "safety": False
        }

    except Exception as e:
        print(f"[Gemini Error] {e}")
        return {
            "reply": "I'm experiencing a technical issue right now. Please try again shortly.",
            "safety": False
        }
