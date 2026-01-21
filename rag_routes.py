@app.post("/api/v1/rag/query")
async def handle_rag_analysis(payload: RagQuery):
    # 1. Search PGVector for the most relevant compliance rules
    vectorstore = PGVector(
        connection=CONNECTION_STRING,
        collection_name=COLLECTION_NAME,
        embeddings=OpenAIEmbeddings()
    )
    
    # Filter by the framework selected in your React dropdown
    relevant_docs = vectorstore.similarity_search(
        payload.query, 
        k=3, 
        filter={"framework": payload.compliance_framework}
    )
    
    context_text = "\n\n".join([doc.page_content for doc in relevant_docs])

    # 2. Send the specific context to Claude
    prompt = f"""
    Use the following compliance excerpts to answer the user query.
    If the answer isn't in the context, say you don't know based on these docs.
    
    CONTEXT:
    {context_text}
    
    USER QUERY: {payload.query}
    """
    
    # ... (rest of your Claude API call using 'prompt')
