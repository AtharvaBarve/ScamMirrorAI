import json
import hashlib
from typing import Any, Dict
import httpx
import asyncio
from app.core.config import settings
from app.services.cache_service import ttl_cache

class ClaudeService:
    """Wrapper around NVIDIA NIM (or Anthropic) API for scam detection."""

    @staticmethod
    def _build_prompt(user_input: str) -> str:
        """
        Build the prompt for the LLM.
        We ask the model to respond with a JSON object containing:
        - verdict: string (e.g., "Likely Scam", "Likely Safe", "Uncertain")
        - explanation: string
        - confidence: float between 0 and 1
        We also provide a couple of few‑shot examples to steer the model.
        """
        few_shot_examples = '''
Examples:
Input: "Congratulations! You've won a free iPhone. Click here to claim now!"
Output: {"verdict":"Likely Scam","explanation":"The message contains typical scam indicators such as unsolicited prize offers and urgency to click a link.","confidence":0.92}

Input: "Hey John, thanks for meeting yesterday. Let's catch up again next week."
Output: {"verdict":"Likely Safe","explanation":"The message is a normal friendly conversation with no signs of fraud or urgency.","confidence":0.95}
'''
        prompt = f"""You are ScamMirror, an expert scam detector.
Given the following input, decide if it is likely a scam, safe, or uncertain.
Provide a short explanation and a confidence score (0-1).
Always respond with valid JSON only, no extra text.

{few_shot_examples}

Input: {user_input}
Output:"""
        return prompt

    @staticmethod
    async def call_nim(user_input: str) -> Dict[str, Any]:
        """
        Call the NVIDIA NIM endpoint (or Anthropic) and return parsed JSON.
        For Day 1 we provide a mock implementation that returns a safe response.
        Replace the mock with a real HTTP call when the API key is available.
        """
        # If no API key is set, return a mock response to keep the demo running.
        if not settings.NIM_API_KEY:
            # Simple heuristic: if the text contains certain keywords, label as scam.
            lowered = user_input.lower()
            scam_keywords = ["free", "prize", "winner", "click here", "urgent", "account suspended", "verify your identity"]
            if any(k in lowered for k in scam_keywords):
                verdict = "Likely Scam"
                confidence = 0.85
                explanation = "The message contains common scam indicators such as offers of free prizes or urgent calls to action."
            else:
                verdict = "Likely Safe"
                confidence = 0.9
                explanation = "The message does not contain obvious scam indicators."
            return {
                "verdict": verdict,
                "explanation": explanation,
                "confidence": confidence,
            }

        # Real implementation (commented out for day 1)
        # prompt = ClaudeService._build_prompt(user_input)
        # async with httpx.AsyncClient(timeout=30.0) as client:
        #     response = await client.post(
        #         settings.NIM_API_URL,
        #         headers={
        #             "Authorization": f"Bearer {settings.NIM_API_KEY}",
        #             "Content-Type": "application/json",
        #         },
        #         json={
        #             "model": settings.NIM_MODEL,
        #             "messages": [{"role": "user", "content": prompt}],
        #             "temperature": 0.0,
        #             "max_tokens": 256,
        #             "response_format": {"type": "json_object"},
        #         },
        #     )
        #     response.raise_for_status()
        #     data = response.json()
        #     # The model returns a
        # extracted = data["choices"][0]["message"]["content"]
        #     try:
        #         result = json.loads(extracted)
        #     except json.JSONDecodeError:
        #         # fallback: wrap text
        #         result = {
        #             "verdict": "Uncertain",
        #             "explanation": "Model returned non‑JSON response.",
        #             "confidence": 0.5,
        #         }
        #     return result