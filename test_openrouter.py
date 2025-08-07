"""
Simple OpenRouter test script for the HackRx system
"""

import asyncio
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from openai import OpenAI
from src.core.config import get_settings
from src.services.document_processor import DocumentProcessor
from src.services.fallback_embedding import FallbackEmbeddingService


async def test_openrouter_llm():
    """Test OpenRouter LLM functionality"""
    print("🤖 Testing OpenRouter LLM...")
    
    try:
        settings = get_settings()
        client = OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url
        )
        
        # Test simple completion
        response = client.chat.completions.create(
            model="openai/gpt-4o-mini",  # Free model on OpenRouter
            messages=[
                {"role": "user", "content": "Hello! Can you help me analyze insurance documents?"}
            ],
            max_tokens=100
        )
        
        answer = response.choices[0].message.content
        if answer is not None:
            print(f"✅ OpenRouter LLM working: {answer[:100]}...")
        else:
            print("⚠️ OpenRouter LLM returned no content.")
        return True
        
    except Exception as e:
        print(f"❌ OpenRouter LLM failed: {e}")
        return False


async def test_document_processing():
    """Test document processing"""
    print("\n📄 Testing document processing...")
    
    try:
        processor = DocumentProcessor()
        
        # Test with sample text instead of URL for now
        sample_text = """
        NATIONAL PARIVAR MEDICLAIM PLUS POLICY
        
        Grace Period: A grace period of thirty days is provided for premium payment 
        after the due date to renew or continue the policy.
        
        Waiting Period: There is a waiting period of thirty-six (36) months of 
        continuous coverage for pre-existing diseases.
        
        Maternity Coverage: The policy covers maternity expenses including childbirth. 
        The female insured person must have been continuously covered for at least 24 months.
        
        Cataract Surgery: The policy has a specific waiting period of two (2) years 
        for cataract surgery.
        """
        
        chunks = processor.chunk_text(sample_text)
        print(f"✅ Document processing works: {len(chunks)} chunks created")
        return chunks
        
    except Exception as e:
        print(f"❌ Document processing failed: {e}")
        return None


async def test_fallback_search():
    """Test fallback embedding service"""
    print("\n🔍 Testing fallback search...")
    
    try:
        embedding_service = FallbackEmbeddingService()
        
        # Use sample chunks
        chunks = [
            "A grace period of thirty days is provided for premium payment after the due date",
            "There is a waiting period of thirty-six months for pre-existing diseases", 
            "The policy covers maternity expenses including childbirth",
            "The policy has a specific waiting period of two years for cataract surgery"
        ]
        
        # Create vector store
        vector_store = await embedding_service.create_vector_store(chunks)
        print(f"✅ Vector store created with {vector_store.ntotal} chunks")
        
        # Test search
        query = "What is the grace period for premium payment?"
        results = await embedding_service.search_similar(query, vector_store, chunks, k=2)
        
        print(f"✅ Search results for '{query}':")
        for chunk, score, idx in results:
            print(f"   Score {score:.3f}: {chunk[:60]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Fallback search failed: {e}")
        return False


async def test_full_pipeline():
    """Test the full question-answering pipeline"""
    print("\n🔄 Testing full pipeline...")
    
    try:
        settings = get_settings()
        
        # Initialize services
        processor = DocumentProcessor()
        embedding_service = FallbackEmbeddingService()
        
        # OpenRouter LLM client
        llm_client = OpenAI(
            api_key=settings.openai_api_key,
            base_url=settings.openai_base_url
        )
        
        # Sample document chunks
        chunks = [
            "A grace period of thirty days is provided for premium payment after the due date to renew or continue the policy without losing continuity benefits.",
            "There is a waiting period of thirty-six (36) months of continuous coverage from the first policy inception for pre-existing diseases and their direct complications to be covered.",
            "Yes, the policy covers maternity expenses, including childbirth and lawful medical termination of pregnancy. To be eligible, the female insured person must have been continuously covered for at least 24 months.",
            "The policy has a specific waiting period of two (2) years for cataract surgery."
        ]
        
        # Create vector store
        vector_store = await embedding_service.create_vector_store(chunks)
        
        # Test questions
        questions = [
            "What is the grace period for premium payment?",
            "What is the waiting period for pre-existing diseases?",
            "Does this policy cover maternity expenses?"
        ]
        
        for question in questions:
            print(f"\n❓ Question: {question}")
            
            # Find relevant chunks
            relevant_chunks = await embedding_service.search_similar(
                question, vector_store, chunks, k=2
            )
            
            # Prepare context
            context = "\n".join([chunk[0] for chunk in relevant_chunks])
            
            # Generate answer using OpenRouter
            response = llm_client.chat.completions.create(
                model="openai/gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at analyzing insurance policies. Answer based only on the provided context."
                    },
                    {
                        "role": "user", 
                        "content": f"Context: {context}\n\nQuestion: {question}\n\nAnswer:"
                    }
                ],
                max_tokens=200
            )
            
            answer = response.choices[0].message.content
            print(f"💡 Answer: {answer}")
        
        print("\n✅ Full pipeline test successful!")
        return True
        
    except Exception as e:
        print(f"❌ Full pipeline test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests"""
    print("🎯 OpenRouter HackRx System Test")
    print("=" * 50)
    
    # Test 1: OpenRouter LLM
    llm_test = await test_openrouter_llm()
    
    # Test 2: Document processing
    doc_test = await test_document_processing()
    
    # Test 3: Fallback search
    search_test = await test_fallback_search()
    
    # Test 4: Full pipeline
    if llm_test and search_test:
        pipeline_test = await test_full_pipeline()
    else:
        pipeline_test = False
    
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"   OpenRouter LLM:    {'✅ PASS' if llm_test else '❌ FAIL'}")
    print(f"   Document Processing: {'✅ PASS' if doc_test else '❌ FAIL'}")
    print(f"   Fallback Search:   {'✅ PASS' if search_test else '❌ FAIL'}")
    print(f"   Full Pipeline:     {'✅ PASS' if pipeline_test else '❌ FAIL'}")
    
    if llm_test and search_test and pipeline_test:
        print("\n🎉 System is ready with OpenRouter!")
        print("\n🚀 Next steps:")
        print("   1. Start server: python -m uvicorn main:app --reload")
        print("   2. Test API endpoint: POST /hackrx/run")
    else:
        print("\n⚠️  Some tests failed. Check your OpenRouter API key.")


if __name__ == "__main__":
    asyncio.run(main())
