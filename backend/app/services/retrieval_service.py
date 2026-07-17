import logging
from typing import Dict, Any, List

from app.services.embedding_service import embedding_service
from app.services.vector_db_service import vector_db

logger = logging.getLogger(__name__)

class RetrievalService:
    """
    Orchestrates the Retrieval-Augmented Generation (RAG) pipeline.
    Queries multiple ChromaDB collections based on the threat classification and embeds the context.
    """
    
    def retrieve_context(self, text: str, classification: Dict[str, Any], extracted_entities: List[Dict[str, Any]]) -> str:
        """
        Retrieves relevant context from multiple collections and formats it for the LLM.
        """
        verdict = classification.get("verdict", "Unknown")
        category = classification.get("category")
        
        # 1. Generate embedding for the input text
        embeddings = embedding_service.generate_embedding(text)
        if not embeddings or len(embeddings) == 0:
            return "No contextual intelligence retrieved (Embedding failed)."
            
        query_embedding = embeddings[0]
        retrieved_contexts = []
        
        logger.info(f"Retrieving context for {verdict} - {category}")
        
        # 2. Query Government Advisories
        # We always want to check for official warnings
        advisories = vector_db.query_collection(
            collection_name="government_advisories",
            query_embedding=query_embedding,
            n_results=2
        )
        for adv in advisories:
            # Only include if similarity is high enough (distance is low in cosine)
            if adv.get("distance", 1.0) < 0.6: 
                retrieved_contexts.append(f"[OFFICIAL ADVISORY - {adv['metadata'].get('source', 'CERT-In')}]: {adv['document']}")
        
        # 3. Query Historical Campaigns
        # Filter by category if one was detected
        where_filter = {"category": category} if category and category != "Unknown" else None
        historical = vector_db.query_collection(
            collection_name="historical_campaigns",
            query_embedding=query_embedding,
            n_results=2,
            where=where_filter
        )
        for hist in historical:
            if hist.get("distance", 1.0) < 0.5:
                retrieved_contexts.append(f"[KNOWN CAMPAIGN - {hist['metadata'].get('campaign_id', 'Unknown')}]: {hist['document']}")
                
        # 4. Query Community Reports
        community = vector_db.query_collection(
            collection_name="community_reports",
            query_embedding=query_embedding,
            n_results=2
        )
        for rep in community:
            if rep.get("distance", 1.0) < 0.4: # Require higher similarity for user reports
                retrieved_contexts.append(f"[COMMUNITY REPORT]: {rep['document']}")
                
        # 5. Format and Rank the final context block
        if not retrieved_contexts:
            return "No matching historical threats or advisories found in the ScamMirror database."
            
        # Deduplicate and limit to top 5 most relevant pieces of context
        unique_contexts = list(dict.fromkeys(retrieved_contexts))[:5]
        
        formatted_context = "### RETRIEVED THREAT INTELLIGENCE ###\n"
        for i, ctx in enumerate(unique_contexts):
            formatted_context += f"{i+1}. {ctx}\n"
            
        logger.debug(f"Retrieved {len(unique_contexts)} context blocks for LLM.")
        return formatted_context

    def seed_mock_data(self):
        """
        Helper method to inject some mock data into ChromaDB so the prototype can demonstrate RAG.
        """
        logger.info("Seeding mock advisories into ChromaDB for RAG demonstration...")
        
        # Seed an RBI Advisory
        adv_text = "Reserve Bank of India (RBI) warns against fraudulent messages claiming account suspension requiring KYC updates via malicious links. Never click unsolicited links claiming to be from your bank."
        adv_emb = embedding_service.generate_embedding(adv_text)[0]
        vector_db.add_document(
            collection_name="government_advisories",
            text=adv_text,
            embedding=adv_emb,
            metadata={"source": "RBI", "category": "Financial Scam"}
        )
        
        # Seed a CERT-In Advisory
        cert_text = "CERT-In alert: Ongoing phishing campaigns impersonating Income Tax Department offering tax refunds. Threat actors request victims to install malicious APKs or visit credential harvesting sites."
        cert_emb = embedding_service.generate_embedding(cert_text)[0]
        vector_db.add_document(
            collection_name="government_advisories",
            text=cert_text,
            embedding=cert_emb,
            metadata={"source": "CERT-In", "category": "Financial Scam"}
        )
        
        # Seed a historical campaign
        camp_text = "Large scale phishing campaign targeting HDFC and SBI users. The message typically reads 'URGENT: Your account has been locked. Click here to verify'. The link redirects to a credential harvesting site."
        camp_emb = embedding_service.generate_embedding(camp_text)[0]
        vector_db.add_document(
            collection_name="historical_campaigns",
            text=camp_text,
            embedding=camp_emb,
            metadata={"campaign_id": "CMP-2025-889", "category": "Financial Scam"}
        )

retrieval_service = RetrievalService()
