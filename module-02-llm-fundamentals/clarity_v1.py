import os
import json
import logging
from dotenv import load_dotenv
from openai import OpenAI
from catalog_loader import load_catalog_from_csv, catalog_to_context
 
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
 
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)
 
def build_system_prompt(catalog_context: str) -> str:
    return f"""You are a friendly and knowledgeable product specialist for Clarity Skincare.
 
PRODUCT CATALOG:
{catalog_context}
 
RULES:
1. Answer questions only using the product information provided above.
2. Never invent ingredients, prices, or product names not in the catalog.
3. If you cannot answer from the catalog, say: "I do not have that information. Please contact us directly."
4. Recommend consulting a dermatologist for medical skin conditions.
5. Keep responses under 100 words unless the customer asks for detail.
6. Do not mention competitor products."""
 
def chat_with_clarity(question: str, conversation_history: list, catalog_context: str) -> str:
    messages = [
        {"role": "system", "content": build_system_prompt(catalog_context)}
    ] + conversation_history + [
        {"role": "user", "content": question}
    ]
 
    response = client.chat.completions.create(
        model="google/gemma-4-26b-a4b-it:free",
        messages=messages,
        temperature=0.1,
        max_tokens=256
    )
 
    answer = response.choices[0].message.content
    tokens_used = response.usage.total_tokens
    logger.info(f"Query: '{question[:50]}...' | Tokens: {tokens_used}")
    return answer
 
def main():
    catalog = load_catalog_from_csv("sample_catalog.csv")
    catalog_context = catalog_to_context(catalog)
    history = []
 
    print("Clarity Skincare Assistant. Type 'quit' to exit.\n")
    while True:
        question = input("You: ").strip()
        if question.lower() == "quit":
            break
 
        answer = chat_with_clarity(question, history, catalog_context)
        print(f"Clarity: {answer}\n")
 
        # Update history for multi-turn conversation
        history.append({"role": "user", "content": question})
        history.append({"role": "assistant", "content": answer})
 
        # Prevent context overflow: keep last 10 exchanges (20 messages)
        if len(history) > 20:
            history = history[-20:]
 
if __name__ == "__main__":
    main()
