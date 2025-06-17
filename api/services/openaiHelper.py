import generativeai as genai
import os
from api.utils.safetyChecker import is_safe

# Configure Generative AI with your API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY")) # Assuming GEMINI_API_KEY for consistency

def generate_response(messages, lang):
    last_msg = messages[-1]['content']
    if not is_safe(last_msg):
        return {"reply": "If you are in crisis, please contact local mental health resources.", "safety": True}

    sys_prompt = {
        "en": "You are a compassionate mental health assistant focused on men's mental health but can also listen to women.....",
        "sw": "Wewe ni msaidizi wa afya ya akili ambaye anawasiliana kwa ufasaha kwa Kiswahili.",
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
        "cs": "Jste asistent duševního zdraví, který plynuje mluví česky.",
        "el": "Είστε βοηθός ψυχικής υγείας που μιλάει άπταιστα ελληνικά.",
        "hu": "Ön egy mentális egészségügyi asszisztens, aki folyékonyan beszél magyarul.",
        "bg": "Вие сте асистент по психично здраве, който говори свободно български.",
        "ro": "Ești un asistent în sănătatea mintală care vorbește fluent română.",
        "vi": "Bạn là một trợ lý sức khỏe tâm thần nói tiếng Việt trôi chảy.",
    }.get(lang, "en")

    model = genai.GenerativeModel('gemini-pro')

    # Convert messages format from OpenAI to Gemini
    # Gemini expects messages as a list of dicts with 'role' and 'parts'
    # The system prompt also needs to be handled.
    # For a simple chat scenario, we can prepend the system prompt to the first user message
    # or handle it as a 'system' role if the model supports it directly in chat.
    # For 'gemini-pro', it's often better to include the system prompt in the first user turn's context.

    # This is a simplified conversion. For more complex conversational flows,
    # you might need to adjust how 'messages' are structured for Gemini.
    gemini_messages = []
    if sys_prompt:
        # Prepend system prompt to the first user message if it exists
        if messages:
            # Create a user message containing the system prompt and the first user message
            # Or if the first message is not 'user', prepend a user message with just the system prompt
            if messages[0]['role'] == 'user':
                gemini_messages.append({'role': 'user', 'parts': [sys_prompt + "\n" + messages[0]['content']]})
                for msg in messages[1:]:
                    gemini_messages.append({'role': msg['role'], 'parts': [msg['content']]})
            else: # If the first message is not user, just add the system prompt as a user message
                gemini_messages.append({'role': 'user', 'parts': [sys_prompt]})
                for msg in messages:
                    gemini_messages.append({'role': msg['role'], 'parts': [msg['content']]})
        else: # If no messages, just start with the system prompt as a user message
            gemini_messages.append({'role': 'user', 'parts': [sys_prompt]})
    else:
        for msg in messages:
            gemini_messages.append({'role': msg['role'], 'parts': [msg['content']]})


    try:
        response = model.generate_content(
            gemini_messages,
            generation_config=genai.types.GenerationConfig(
                temperature=0.7,
                max_output_tokens=250 # Corresponds to max_tokens in OpenAI
            )
        )
        return {"reply": response.text, "safety": False}
    except Exception as e:
        # Handle potential errors from the Generative AI API, e.g., safety concerns, rate limits
        print(f"Error generating content: {e}")
        return {"reply": "I'm sorry, I couldn't generate a response at this time. Please try again later.", "safety": True}

