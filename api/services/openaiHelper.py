import openai
import os
from typing import Dict, Optional, List
from .safetyChecker import SafetyChecker

openai.api_key = os.getenv("OPENAI_API_KEY")
class OpenAIClient:
    def __init__(self):
        self.model = "gpt-3.5-turbo"
        

            
    def _get_system_prompt(self, userId: Optional[str] = None, language: str = "en") -> list:
        prompts = {
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
            "cs": "Jste asistent duševního zdraví, který plynně mluví česky.",
            "el": "Είστε βοηθός ψυχικής υγείας που μιλάει άπταιστα ελληνικά.",
            "hu": "Ön egy mentális egészségügyi asszisztens, aki folyékonyan beszél magyarul.",
            "ar": "أنت مساعد الصحة النفسية الذي يتحدث العربية بطلاقة.",
            "bg": "Вие сте асистент по психично здраве, който говори свободно български.",
            "ro": "Ești un asistent în sănătatea mintală care vorbește fluent română.",
            "vi": "Bạn là một trợ lý sức khỏe tâm thần nói tiếng Việt trôi chảy.",  
        }
        prompts = prompts.get(language, prompts["en"])
        if userId:
            prompts += f" User ID: {userId}"
            
        return prompts

    def generateResponse(self, messages: List[Dict], language: str = "en", userId: Optional[str] = None) -> Dict:
        try:
            lastUseramessage = next((msg for msg in reversed(messages) if msg['role'] == 'user'), None)
            if lastUseramessage and not SafetyChecker.checkSafety(lastUseramessage['content']):
                return {
                    "reply": "It seems like you might be in distress. If you are in crisis please reachout to a mental health profession, if you don't have any I have a few suggestions for you.",
                    "safety_triggered":True
                }
                
            messages.insert(0,{
                "role": "system",
                "content":self._get_system_prompt(language, userId)
            })
            response = openai.ChatCompletion.create(
                model=self.default_model,
                messages=self._add_system_prompt(messages, userId),
                temperature=0.7,
                max_tokens=254,
            )
            return {
                "reply": response.choices[0].message['content'],
                "safety_triggered": False
            }
        except Exception as e:
            return {
                "reply": "I am having trouble processing your request. Please try again later.", 
                "error": str(e),
                "safety_triggered": False
   
            }        