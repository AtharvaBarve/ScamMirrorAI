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

    @staticmethod
    async def get_explanation_and_actions(threat_assessment: Dict[str, Any], original_text: str, rag_context: str = "") -> Dict[str, Any]:
        """
        Get only explanation and recommended actions from NIM, given a threat assessment and RAG context.
        The NIM must NOT modify verdict, confidence, category, or risk_factors.
        """
        # If no API key is set, use heuristic fallback for explanation and actions.
        if not settings.NIM_API_KEY:
            return ClaudeService._heuristic_explanation_fallback(threat_assessment, original_text, rag_context)

        start_time = time.time()
        # Build the prompt for explanation only
        verdict = threat_assessment.get("verdict", "Unknown")
        confidence = threat_assessment.get("confidence", 0.0)
        category = threat_assessment.get("category", "Unknown")
        risk_factors = threat_assessment.get("risk_factors", [])
        # Format the risk factors for the prompt
        risk_factors_str = ", ".join(risk_factors) if risk_factors else "none"

        # We also want to include the signals? The threat_assessment has a 'signals' key with details.
        # We'll format a brief description of the signals.
        signals_detail = []
        for s in threat_assessment.get("signals", []):
            signals_detail.append(f"- {s['name']}: {s['description']} (evidence: {s['evidence']})")
        signals_str = "\n".join(signals_detail) if signals_detail else "none"

        prompt = f"""You are ScamMirror, an expert scam explainer and threat intelligence analyst.
A message has already been classified as {verdict} with confidence {confidence}.
The category is {category}.
The detected risk factors are: {risk_factors_str}.
The detailed threat signals are:
{signals_str}

{rag_context}

Your ONLY responsibility is to:
1. Explain WHY this message was classified this way, based on the detected threat signals.
2. If any RETRIEVED THREAT INTELLIGENCE (like CERT-In, RBI advisories, or known campaigns) is provided above, explicitly cite it in your explanation to back up your claims.
3. Give actionable recommendations for the user.

You MUST NOT change the verdict, confidence, or category.
You MUST NOT invent additional threat signals.

Provide your response as a JSON object with only two keys: "explanation" and "recommended_actions".

Example:
Input: "Congratulations! You've won a free iPhone. Click here to claim now!"
(Assume classification: Likely Scam, category: Financial Scam, signals: [Urgency, Financial Incentive])
Output: {{"explanation": "The message contains urgent language and promises of free prizes, which are common scam tactics. This aligns with recent CERT-In advisories regarding fake prize schemes.", "recommended_actions": ["Do not click any links", "Delete the message"]}}

Now, here is the actual message:
\"\"\"{original_text}\"\"\"

Remember: only explain and recommend, do not question the classification.
"""
        payload = {
            "model": settings.NIM_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.0,
            "max_tokens": 128,  # We only need explanation and actions, so shorter is fine
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
                        # We only expect "explanation" and "recommended_actions"
                        # If missing, provide fallback
                        explanation = result.get("explanation", "").strip()
                        actions = result.get("recommended_actions", [])
                        # Ensure actions is a list of strings
                        if not isinstance(actions, list):
                            actions = [str(actions)]
                        # Filter out empty strings
                        actions = [a.strip() for a in actions if a.strip()]
                        return {
                            "explanation": explanation,
                            "recommended_actions": actions,
                        }
                    except (json.JSONDecodeError, ValueError, KeyError) as e:
                        # If JSON parsing fails, we will fallback after retries?
                        pass
            except (httpx.HTTPStatusError, httpx.RequestError) as e:
                # Log the error? For now, just continue to retry if retries left.
                pass

            # If we are here, the attempt failed; wait before retrying (except on last attempt)
            if attempt < max_retries - 1:
                await asyncio.sleep(retry_delay * (attempt + 1))  # simple backoff

        # All retries exhausted or we encountered a non-retryable error; fallback to heuristic.
        return ClaudeService._heuristic_explanation_fallback(threat_assessment, original_text)

    @staticmethod
    def _heuristic_explanation_fallback(threat_assessment: Dict[str, Any], original_text: str, rag_context: str = "") -> Dict[str, Any]:
        """
        Fallback explanation when NIM is unavailable.
        Generates a basic explanation based on the threat assessment.
        """
        verdict = threat_assessment.get("verdict", "Unknown")
        confidence = threat_assessment.get("confidence", 0.0)
        risk_factors = threat_assessment.get("risk_factors", [])
        signals = threat_assessment.get("signals", [])

        # Build explanation
        if verdict == "Likely Scam":
            explanation = f"The message was classified as a likely scam due to the detection of risk factors such as: {', '.join(risk_factors) if risk_factors else 'suspicious patterns'}."
        elif verdict == "Likely Safe":
            explanation = "The message was classified as likely safe as no significant threat signals were detected."
        else:  # Uncertain
            explanation = "The classification is uncertain due to weak or conflicting signals."

        # If we have signal details, we can add more
        if signals:
            signal_descs = [f"{s.get('name', '')}: {s.get('description', '')}" for s in signals if s.get("description")]
            if signal_descs:
                explanation += " Specifically, it detected: " + "; ".join(signal_descs) + "."

        if rag_context:
            explanation += "\n\n(NIM is offline. Heuristic RAG Data Dump):\n" + rag_context

        # Provide some generic actions based on verdict
        if verdict == "Likely Scam":
            recommended_actions = [
                "Do not click any links or download attachments.",
                "Do not provide any personal or financial information.",
                "Delete the message and block the sender if possible."
            ]
        elif verdict == "Likely Safe":
            recommended_actions = [
                "The message appears safe, but always exercise caution with unsolicited messages."
            ]
        else:
            recommended_actions = [
                "Exercise caution when interacting with this message.",
                "Verify the sender through an independent channel if possible."
            ]

        return {
            "explanation": explanation,
            "recommended_actions": recommended_actions,
        }