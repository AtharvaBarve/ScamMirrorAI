import json
import time
from typing import Any, Dict, List
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
        - category: string (e.g., "Financial Scam", "Phishing", "Malware", "Safe")
        - risk_factors: list of strings (e.g., ["Urgency", "Unsolicited offer"])
        - recommended_actions: list of strings (e.g., ["Do not click any links", "Delete the message"])
        We also provide a couple of few‑shot examples to steer the model.
        """
        few_shot_examples = '''
Examples:
Input: "Congratulations! You've won a free iPhone. Click here to claim now!"
Output: {"verdict":"Likely Scam","explanation":"The message contains typical scam indicators such as unsolicited prize offers and urgency to click a link.","confidence":0.92,"category":"Financial Scam","risk_factors":["Unsolicited offer","Urgency"],"recommended_actions":["Do not click any links","Delete the message"]}

Input: "Hey John, thanks for meeting yesterday. Let's catch up again next week."
Output: {"verdict":"Likely Safe","explanation":"The message is a normal friendly conversation with no signs of fraud or urgency.","confidence":0.95,"category":"Safe","risk_factors":[],"recommended_actions":[]}
'''
        prompt = f"""You are ScamMirror, an expert scam detector.
Given the following input, decide if it is likely a scam, safe, or uncertain.
Provide a short explanation, a confidence score (0-1), a category, list of risk factors, and recommended actions.
Always respond with valid JSON only, no extra text.

{few_shot_examples}

Input: {user_input}
Output:"""
        return prompt

    @staticmethod
    def _heuristic_fallback(user_input: str) -> Dict[str, Any]:
        """
        Simple heuristic fallback when NIM is unavailable.
        """
        lowered = user_input.lower()
        scam_keywords = ["free", "prize", "winner", "click here", "urgent", "account suspended", "verify your identity"]
        if any(k in lowered for k in scam_keywords):
            verdict = "Likely Scam"
            confidence = 0.85
            explanation = "The message contains common scam indicators such as offers of free prizes or urgent calls to action."
            category = "Financial Scam"
            risk_factors = ["Unsolicited offer", "Urgency"]
            recommended_actions = ["Do not click any links", "Delete the message"]
        else:
            verdict = "Likely Safe"
            confidence = 0.9
            explanation = "The message does not contain obvious scam indicators."
            category = "Safe"
            risk_factors = []
            recommended_actions = []
        return {
            "verdict": verdict,
            "explanation": explanation,
            "confidence": float(confidence),
            "category": category,
            "risk_factors": risk_factors,
            "recommended_actions": recommended_actions,
        }

    @staticmethod
    async def call_nim(user_input: str) -> Dict[str, Any]:
        """
        Call the NVIDIA NIM endpoint and return parsed JSON.
        If the API key is missing or the request fails after retries,
        fall back to the heuristic.
        """
        # If no API key is set, use heuristic immediately.
        if not settings.NIM_API_KEY:
            return ClaudeService._heuristic_fallback(user_input)

        start_time = time.time()
        payload = {
            "model": settings.NIM_MODEL,
            "messages": [{"role": "user", "content": ClaudeService._build_prompt(user_input)}],
            "temperature": 0.0,
            "max_tokens": 256,
            "response_format": {"type": "json_object"},
        }
        max_retries = 3
        retry_delay = 1  # seconds

        for attempt in range(max_retries):
            try:
                async with httpx.AsyncClient(timeout=30.0) as client:
                    response = await client.post(
                        settings.NIM_API_URL,
                        headers={
                            "Authorization": f"Bearer {settings.NIM_API_KEY}",
                            "Content-Type": "application/json",
                        },
                        json=payload,
                    )
                    # If we get a 4xx client error, break and fallback (not retryable)
                    if 400 <= response.status_code < 500:
                        break
                    response.raise_for_status()  # Raise for 5xx or other non-2xx
                    data = response.json()
                    # Extract the content from the first choice
                    extracted = data["choices"][0]["message"]["content"]
                    try:
                        result = json.loads(extracted)
                        # Ensure we have all expected fields; if missing, fill with fallback defaults
                        expected_keys = ["verdict", "explanation", "confidence", "category", "risk_factors", "recommended_actions"]
                        for key in expected_keys:
                            if key not in result:
                                # If missing, we will fill from fallback for consistency
                                fallback = ClaudeService._heuristic_fallback(user_input)
                                result[key] = fallback.get(key)
                        # Ensure confidence is float between 0 and 1
                        conf = float(result["confidence"])
                        if not (0.0 <= conf <= 1.0):
                            # Clamp or fallback
                            fallback = ClaudeService._heuristic_fallback(user_input)
                            conf = fallback["confidence"]
                        result["confidence"] = conf
                        # Add processing time
                        result["processing_time"] = time.time() - start_time
                        return result
                    except (json.JSONDecodeError, ValueError, KeyError) as e:
                        # If JSON parsing fails or missing keys, we will fallback after retries?
                        # For now, treat as failure and will retry (maybe intermittent)
                        pass
            except (httpx.HTTPStatusError, httpx.RequestError) as e:
                # Log the error? For now, just continue to retry if retries left.
                pass

            # If we are here, the attempt failed; wait before retrying (except on last attempt)
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay * (attempt + 1))  # simple backoff

        # All retries exhausted or we encountered a non-retryable error; fallback to heuristic.
        fallback = ClaudeService._heuristic_fallback(user_input)
        fallback["processing_time"] = time.time() - start_time
        return fallback