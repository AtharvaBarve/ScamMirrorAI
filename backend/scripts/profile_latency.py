import asyncio
import time
import httpx
import json

async def profile_latency():
    print("=== API LATENCY PROFILING ===")
    
    url = "http://127.0.0.1:8000/api/v1/analyze"
    payload = {"text": "URGENT: Your HDFC bank account is locked. Click here to verify your identity: http://hdfc-update-kyc.com"}
    
    times = []
    
    async with httpx.AsyncClient() as client:
        # Warmup
        try:
            await client.post(url, json=payload, timeout=20.0)
        except Exception:
            print("Backend not running. Please start the FastAPI server on port 8000 to profile.")
            return

        for i in range(5):
            start = time.time()
            resp = await client.post(url, json=payload, timeout=20.0)
            end = time.time()
            elapsed = end - start
            times.append(elapsed)
            print(f"Request {i+1}: {elapsed:.3f}s")
            
    avg = sum(times) / len(times)
    print(f"\nAverage End-to-End Latency: {avg:.3f}s")
    
    if avg > 2.0:
        print("Warning: Latency is high. Consider caching classifier or optimizing ChromaDB queries.")
    else:
        print("Performance is excellent for local inference!")

if __name__ == "__main__":
    asyncio.run(profile_latency())
