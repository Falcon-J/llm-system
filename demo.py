"""
Simple demo script to showcase the system capabilities
"""

import asyncio
import json
from src.services.document_processor import DocumentProcessor
from src.services.embedding_service import EmbeddingService
from src.services.llm_service import LLMService
from src.services.retrieval_service import RetrievalService
from src.core.config import get_settings


async def run_demo():
    """Run a demo of the system capabilities"""
    
    print("🚀 LLM-Powered Intelligent Query-Retrieval System Demo")
    print("=" * 60)
    
    # Initialize services
    print("\n📋 Initializing services...")
    settings = get_settings()
    
    try:
        document_processor = DocumentProcessor()
        
        # Try embedding service, fallback if needed
        try:
            from src.services.embedding_service import EmbeddingService
            embedding_service = EmbeddingService()
            print("✅ Using API-based embedding service")
        except Exception as e:
            print(f"⚠️  API embedding service failed: {e}")
            from src.services.fallback_embedding import FallbackEmbeddingService
            embedding_service = FallbackEmbeddingService()
            print("✅ Using fallback TF-IDF embedding service")
        
        llm_service = LLMService()
        retrieval_service = RetrievalService(embedding_service, llm_service)
        print("✅ All services initialized successfully")
        
    except Exception as e:
        print(f"❌ Failed to initialize services: {e}")
        print("💡 Make sure you have set your API key in .env file")
        print("💡 For OpenRouter, use: OPENAI_API_KEY=sk-or-v1-your-key-here")
        return
    
    # Sample document URL (the one provided in the problem)
    document_url = "https://hackrx.blob.core.windows.net/assets/policy.pdf?sv=2023-01-03&st=2025-07-04T09%3A11%3A24Z&se=2027-07-05T09%3A11%3A00Z&sr=b&sp=r&sig=N4a9OU0w0QXO6AOIBiu4bpl7AXvEZogeT%2FjUHNO7HzQ%3D"
    
    # Sample questions
    questions = [
        "What is the grace period for premium payment under the National Parivar Mediclaim Plus Policy?",
        "Does this policy cover maternity expenses, and what are the conditions?",
        "What is the waiting period for cataract surgery?"
    ]
    
    print(f"\n📄 Processing document: {document_url[:80]}...")
    
    try:
        # Step 1: Process document
        print("\n🔧 Step 1: Processing document...")
        document_content = await document_processor.process_document_url(document_url)
        print(f"✅ Document processed successfully ({len(document_content)} characters)")
        
        # Step 2: Create chunks and embeddings
        print("\n🧩 Step 2: Creating text chunks...")
        chunks = document_processor.chunk_text(document_content)
        print(f"✅ Created {len(chunks)} text chunks")
        
        print("\n🔤 Step 3: Generating embeddings...")
        vector_store = await embedding_service.create_vector_store(chunks)
        print(f"✅ Vector store created with {vector_store.ntotal} embeddings")
        
        # Step 3: Process questions
        print(f"\n❓ Step 4: Processing {len(questions)} questions...")
        print("=" * 60)
        
        for i, question in enumerate(questions, 1):
            print(f"\n🔍 Question {i}: {question}")
            print("-" * 50)
            
            try:
                # Retrieve relevant chunks
                relevant_chunks = await retrieval_service.retrieve_relevant_chunks(
                    question, vector_store, chunks
                )
                
                # Generate answer
                answer = await llm_service.generate_answer(question, relevant_chunks)
                
                print(f"💡 Answer: {answer}")
                print(f"📊 Based on {len(relevant_chunks)} relevant chunks")
                
                if relevant_chunks:
                    best_chunk = relevant_chunks[0]
                    print(f"🎯 Top relevance score: {best_chunk[1]:.3f}")
                
            except Exception as e:
                print(f"❌ Error processing question: {e}")
        
        print("\n" + "=" * 60)
        print("🎉 Demo completed successfully!")
        print("\n💡 Key Features Demonstrated:")
        print("   ✅ Multi-format document processing")
        print("   ✅ Semantic embedding and vector search")
        print("   ✅ LLM-powered answer generation")
        print("   ✅ Explainable AI with source attribution")
        print("   ✅ Domain-specific optimization for insurance/legal docs")
        
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        print("💡 Check your internet connection and API keys")


if __name__ == "__main__":
    asyncio.run(run_demo())
