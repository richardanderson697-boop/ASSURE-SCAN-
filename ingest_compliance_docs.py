import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings # Or Anthropic/HuggingFace
from langchain_postgres.vectorstores import PGVector

# Railway provides the DATABASE_URL automatically if linked
CONNECTION_STRING = os.getenv("DATABASE_URL")
COLLECTION_NAME = "compliance_frameworks"

def ingest_compliance_pdf(file_path: str, framework_name: str):
    # 1. Load the PDF (e.g., SOC2_Requirements.pdf)
    loader = PyPDFLoader(file_path)
    docs = loader.load()

    # 2. Split text into manageable chunks
    # We use overlaps so context isn't lost between chunks
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    chunks = text_splitter.split_documents(docs)

    # 3. Add metadata so the RAG engine can filter by framework
    for chunk in chunks:
        chunk.metadata["framework"] = framework_name

    # 4. Store in PGVector
    embeddings = OpenAIEmbeddings() # Ensure OPENAI_API_KEY is in Railway vars
    PGVector.from_documents(
        embedding=embeddings,
        documents=chunks,
        connection=CONNECTION_STRING,
        collection_name=COLLECTION_NAME,
        use_jsonb=True,
    )
    print(f"✅ Successfully ingested {len(chunks)} chunks for {framework_name}")

if __name__ == "__main__":
    ingest_compliance_pdf("./docs/soc2_manual.pdf", "soc2")
