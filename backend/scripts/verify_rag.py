import asyncio
import os
import shutil
from typing import Dict, Any

def run_verification():
    print("--- Phase 3 RAG Verification ---")
    
    # Clean old db for fresh test
    db_path = os.path.join(os.path.dirname(__file__), "../chroma_db")
    
    from app.services.vector_db_service import VectorDBService
    from app.services.embedding_service import embedding_service
    from app.services.retrieval_service import retrieval_service
    from app.services.hybrid_service import hybrid_service
    
    # 1. Initialize and check collections
    print("\n1. Testing ChromaDB Initialization...")
    vector_db = VectorDBService()
    if vector_db.client is not None:
        print("✅ ChromaDB initialized correctly.")
    else:
        print("❌ ChromaDB failed to initialize.")
        
    collections = vector_db.collections.keys()
    print(f"✅ Collections found: {list(collections)}")

    # 3. Test embeddings
    print("\n3. Testing Embedding Generation...")
    text = "URGENT: Your HDFC account is blocked. Update KYC at http://fake-hdfc.com"
    embedding = embedding_service.generate_embedding(text)
    if embedding and len(embedding[0]) > 0:
        print(f"✅ Embedding generated successfully (dim: {len(embedding[0])})")
    else:
        print("❌ Embedding generation failed.")

    # Add mock data to test retrieval
    print("\nSeeding data for retrieval tests...")
    retrieval_service.seed_mock_data()
    vector_db.add_document(
        "community_reports", 
        "Got a fake SMS about HDFC KYC update from +91-9876543210. Link goes to phishing site.", 
        embedding_service.generate_embedding("Got a fake SMS about HDFC KYC update from +91-9876543210. Link goes to phishing site.")[0], 
        {"source": "user_report"}
    )

    # 2. Test persistence (re-initialize)
    print("\n2. Testing Collection Persistence...")
    vector_db_2 = VectorDBService()
    count = vector_db_2.collections["government_advisories"].count()
    if count > 0:
        print(f"✅ Collections persisted after re-initialization (Found {count} docs).")
    else:
        print("❌ Persistence failed.")

    # 4-8. Test Retrieval
    print("\n4-8. Testing Retrieval Logic (Multi-faceted & Category Aware)...")
    classification = {"verdict": "Likely Scam", "category": "Financial Scam"}
    context = retrieval_service.retrieve_context(text, classification, [])
    
    if "OFFICIAL ADVISORY" in context and ("RBI" in context or "CERT-In" in context):
        print("✅ Government advisories successfully retrieved.")
    else:
        print("❌ Government advisories NOT retrieved.")
        
    if "COMMUNITY REPORT" in context:
        print("✅ Community reports successfully retrieved.")
    else:
        print("❌ Community reports NOT retrieved.")
        
    if "KNOWN CAMPAIGN" in context:
        print("✅ Historical campaigns successfully retrieved.")
    else:
        print("❌ Historical campaigns NOT retrieved.")

    # 9. Test LLM prompt context injection
    print("\n9. Testing LLM Prompt Generation with Context...")
    from app.services.claude_service import ClaudeService
    # We will just test the heuristic fallback string since it builds the context into the explanation when offline
    fallback_res = ClaudeService._heuristic_explanation_fallback({"verdict": "Likely Scam"}, text, rag_context=context)
    if "RETRIEVED THREAT INTELLIGENCE" in fallback_res["explanation"]:
        print("✅ Retrieved context successfully injected into LLM fallback prompt.")
    else:
        print("❌ Retrieved context missing from prompt.")

    # 10. Test hybrid service pipeline end-to-end
    print("\n10. Testing Backend Pipeline (Hybrid Service)...")
    try:
        result = asyncio.run(hybrid_service.analyze("text", text))
        if "verdict" in result and "explanation" in result:
            print("✅ Backend pipeline passed and returned valid API schema.")
        else:
            print("❌ Backend pipeline returned invalid schema.")
    except Exception as e:
        print(f"❌ Backend pipeline failed: {e}")

if __name__ == "__main__":
    run_verification()
