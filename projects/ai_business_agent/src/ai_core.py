import os
import aiohttp
import logging

logger = logging.getLogger("AI_AGENT")

class AIBusinessAgent:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

    async def get_response(self, user_query: str, context: str):
        # Логика RAG: подмешиваем контекст из базы знаний
        prompt = f"Контекст: {context}\n\nВопрос клиента: {user_query}"
        
        payload = {
            "contents": [{"parts": [{"text": prompt}]}]
        }
        
        # Интеграция через aiohttp для сохранения асинхронности
        async with aiohttp.ClientSession() as session:
            async with session.post(f"{self.api_url}?key={self.api_key}", json=payload) as resp:
                result = await resp.json()
                logger.info("AI response generated and logged.")
                return result['candidates'][0]['content']['parts'][0]['text']
