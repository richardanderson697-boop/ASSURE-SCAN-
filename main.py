
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import Optional, List
import anthropic
import os
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Assure Scanner RAG API",
    description="RAG-powered compliance and security analysis using Claude",
    version="1.0.0"
)

# Optional: Simple API key auth for internal calls
INTERNAL_API_KEY = os.getenv("INTERNAL_API_KEY")  # Set in Railway Variables

api_key_header = APIKeyHeader(name="X-Internal-API-Key", auto_error=False)

async def verify_internal_key(api_key: str = Depends(api_key_header)):
    if not INTERNAL_API_KEY:
        logger.error("INTERNAL_API_KEY not set in environment")
        raise HTTPException(status_code=500, detail="Server configuration error")
    if api_key != INTERNAL_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key

# Request Model (matches your frontend fetch body)
class RagQuery(BaseModel):
    query: str
    compliance_framework: str
    code_context: Optional[str] = None
    include_examples: bool = True

# Response Model (makes Swagger docs better + type safety)
class RagResponse(BaseModel):
    answer: str
    confidence: str
    sources: List[str]
    timestamp: str

@app.post(
    "/api/v1/rag/query",
    response_model=RagResponse,
    summary="Analyze code for compliance & security gaps using Claude",
    dependencies=[Depends(verify_internal_key)]  # Protect endpoint
)
async def handle_rag_analysis(payload: RagQuery):
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        logger.error("ANTHROPIC_API_KEY not set")
        raise HTTPException(status_code=500, detail="AI service not configured")

    client = anthropic.Anthropic(api_key=api_key)

    # Dynamic system prompt
    system_prompt = f"""
You are the Assure Scanner Security & Compliance Engine.
Primary focus: {payload.compliance_framework}
Task: Analyze the provided code/query for vulnerabilities, regulatory gaps, best practices.
{ "Include practical code examples." if payload.include_examples else "" }
Context provided (if any): {payload.code_context or "None"}
Respond concisely, professionally, and with actionable recommendations.
"""

    try:
        logger.info(f"Processing RAG query for framework: {payload.compliance_framework}")

        response = client.messages.create(
            model=os.getenv("ANTHROPIC_MODEL", "claude-3-5-sonnet-20240620"),
            max_tokens=int(os.getenv("MAX_TOKENS", "2000")),
            system=system_prompt,
            messages=[{"role": "user", "content": payload.query}]
        )

        answer = response.content[0].text.strip()

        return RagResponse(
            answer=answer,
            confidence="High",
            sources=["Anthropic Claude", f"{payload.compliance_framework} Framework", "Internal Security Guidelines"],
            timestamp=datetime.utcnow().isoformat()
        )

    except anthropic.APIError as e:
        logger.error(f"Anthropic API error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"AI service error: {str(e)}")
    except Exception as e:
        logger.exception("Unexpected error in RAG analysis")
        raise HTTPException(status_code=500, detail="Internal server error")
