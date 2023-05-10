from fastapi import FastAPI
from pydantic import BaseModel
import openai
from dotenv import load_dotenv
import os
from wale import Wale
app = FastAPI()

# Load the OpenAI API key from the .env file
load_dotenv()
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
WALE_API_KEY = os.environ.get("WALE_API_KEY")
WALE_API_ROOT = os.environ.get("WALE_API_ROOT")
openai.api_key = OPENAI_API_KEY

print('WALE_API_ROOT', WALE_API_ROOT)
print('WALE_API_KEY', WALE_API_KEY)
if OPENAI_API_KEY is None:
    print("WARNING: No OpenAI API key found. Defaulting to a dummy summary.")

if WALE_API_KEY is None:
    print("FATAL: No Wale API key found. Need to set the Wale API key in the .env file")

logger = Wale(
    api_key=WALE_API_KEY,
    api_root=WALE_API_ROOT,
)
class SummarizeRequest(BaseModel):
    document: str

@app.post("/summarize")
async def summarize(request: SummarizeRequest):
    document = request.document
    if OPENAI_API_KEY is not None:
        response = openai.Completion.create(
            engine="davinci",
            prompt=f"Please summarize the following document for a 10 year old. Input: \n\n{document}. \n\nSummary:",
            temperature=0.5,
            max_tokens=100,
            n = 1,
            stop=None
        )
        summary = response.choices[0].text.strip()
        total_tokens = response.usage["total_tokens"]
    else:
        summary = 'Default summary: ' + document
        total_tokens = len(summary)

    log_obj = logger.log(
        inputs={"document": document},
        output=summary,
        task_id="summarize",
        model_config={
            "model": "davinci",
            "provider": "openai",
            "temperature": 0.5,
            "max_tokens": 100,
        },
        person_id = "pid-person123",
        total_tokens=total_tokens,
    )
    if ('error' in log_obj):
        print('error', log_obj['error'])
    else:
        print('log_id', log_obj['id'])
    return {"summary": summary}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
