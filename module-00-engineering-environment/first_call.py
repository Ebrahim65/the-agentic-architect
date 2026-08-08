import os
import time
import logging
from dotenv import load_dotenv
from openai import OpenAI
 
# Load environment variables from .env
load_dotenv()

# Configure logging: writes to both a file and the console
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)
 
# The OpenAI client works with OpenRouter by changing the base_url
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)
 
logger.info("Starting API call")
start_time = time.time()
 
response = client.chat.completions.create(
    model="google/gemma-4-26b-a4b-it:free",
    messages=[
        {"role": "user", "content": "Respond with exactly: Hello, agent world."}
    ]
)
 
duration = time.time() - start_time
content = response.choices[0].message.content
 
logger.info(f"Call completed in {duration:.2f} seconds")
logger.info(f"Response: {content}")
logger.info(f"Tokens used: {response.usage.total_tokens}")





