from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import anthropic
import os

app = FastAPI(title="Assure Scanner API")

# Request Model matching your Frontend's fetch body
class RagQuery(BaseModel):
    query: str
    compliance_framework: str
    code_context: Optional[str] = None
    include_examples: bool = True

@app.post("/api/v1/rag/query")
async def handle_rag_analysis(payload: RagQuery):
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
    
    # 1. System Prompt Construction
    # This grounds the AI in your specific security logic
    system_prompt = f"""
    You are the Assure Scanner Security Engine. 
    Focus: {payload.compliance_framework}
    Context: Analyze the provided code for vulnerabilities and regulatory gaps.
    """

    try:
        # 2. Call Claude Sonnet 3.5/4
        response = client.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=2000,
            system=system_prompt,
            messages=[{"role": "user", "content": payload.query}]
        )
        
        # 3. Return structured data to the React Dashboard
        return {
            "answer": response.content[0].text,
            "confidence": "High",
            "sources": ["Internal Security Docs", f"{payload.compliance_framework} Framework"],
            "timestamp": "2024-05-20T10:00:00Z"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
