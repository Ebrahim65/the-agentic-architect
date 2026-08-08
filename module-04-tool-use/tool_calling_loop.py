import os
import json
import logging
from openai import OpenAI
from dotenv import load_dotenv
 
load_dotenv()
logger = logging.getLogger(__name__)
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.getenv("OPENROUTER_API_KEY"),
)
 
# --- Tool implementations ---
 
def lookup_product(product_name: str, information_needed: str) -> str:
    """
    Look up product information from the catalog.
    Returns a formatted string with the requested information.
    """
    # In production this queries a database or vector store
    # For now, a simple dict lookup
    catalog = {
        "Glow Serum": {
            "price": 349.00,
            "ingredients": ["Vitamin C 15%", "Niacinamide 5%", "Hyaluronic Acid"],
            "suitable_for": ["oily", "combination"],
            "in_stock": True
        }
    }
 
    if product_name not in catalog:
        return f"Product '{product_name}' not found in catalog."
 
    product = catalog[product_name]
 
    if information_needed == "price":
        return f"{product_name} costs R{product['price']:.2f}."
    elif information_needed == "ingredients":
        return f"{product_name} ingredients: {', '.join(product['ingredients'])}."
    elif information_needed == "suitability":
        return f"{product_name} is suitable for: {', '.join(product['suitable_for'])} skin types."
    elif information_needed == "stock":
        status = "in stock" if product["in_stock"] else "out of stock"
        return f"{product_name} is currently {status}."
    else:  # full_details
        return json.dumps(product, indent=2)
    
product_lookup_tool = {
    "type": "function",
    "function": {
        "name": "lookup_product",
        "description": (
            "Look up detailed information about a specific Clarity Skincare product. "
            "Use this when the customer asks about a specific product's ingredients, "
            "price, suitability for a skin type, or stock availability. "
            "Do NOT use this for general skincare advice not related to a product."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "product_name": {
                    "type": "string",
                    "description": "The exact product name as it appears in the catalog, e.g. 'Glow Serum'"
                },
                "information_needed": {
                    "type": "string",
                    "enum": ["ingredients", "price", "suitability", "stock", "full_details"],
                    "description": "What specific information the customer needs about this product"
                }
            },
            "required": ["product_name", "information_needed"]
        }
    }
}

 
# Map tool names to functions
TOOL_MAP = {
    "lookup_product": lookup_product,
}
 
def execute_tool(tool_name: str, arguments: dict) -> str:
    """Execute a tool by name with the given arguments."""
    if tool_name not in TOOL_MAP:
        return f"Error: Tool '{tool_name}' not found."
    try:
        result = TOOL_MAP[tool_name](**arguments)
        logger.info(f"Tool '{tool_name}' called with {arguments} → success")
        return result
    except Exception as e:
        logger.error(f"Tool '{tool_name}' failed: {e}")
        return f"Tool execution failed: {str(e)}"
 
# --- The agent loop ---
 
def run_agent(user_message: str, tools: list, system_prompt: str) -> str:
    """
    Run a single-turn agent interaction.
    Handles tool calls automatically and returns the final text response.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_message}
    ]
 
    max_iterations = 5  # Prevent infinite loops
    for iteration in range(max_iterations):
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b:free",
            messages=messages,
            tools=tools,
            tool_choice="auto",
            temperature=0.1
        )
 
        msg = response.choices[0].message
 
        # Case 1: No tool calls - we have the final answer
        if not msg.tool_calls:
            return msg.content
 
        # Case 2: Tool calls - execute each and add results to messages
        # First, add the assistant's message (with tool calls) to history
        messages.append({
            "role": "assistant",
            "content": msg.content,
            "tool_calls": [
                {
                    "id": tc.id,
                    "type": "function",
                    "function": {
                        "name": tc.function.name,
                        "arguments": tc.function.arguments
                    }
                }
                for tc in msg.tool_calls
            ]
        })
 
        # Then add each tool result
        for tool_call in msg.tool_calls:
            tool_name = tool_call.function.name
            try:
                arguments = json.loads(tool_call.function.arguments)
            except json.JSONDecodeError:
                arguments = {}
 
            result = execute_tool(tool_name, arguments)
            logger.info(f"Iteration {iteration}: {tool_name}({arguments}) → {result[:100]}")
 
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "content": result
            })
 
    # If we exit the loop without a final answer, force synthesis
    return "I was unable to complete that request. Please try rephrasing your question."
 
# Test it
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    system_prompt = "You are a Clarity Skincare product specialist. Use the lookup_product tool to answer product questions."
    tools = [product_lookup_tool]
 
    queries = [
        "What's the price of the Glow Serum?",
        "Is the Glow Serum good for my oily skin?",
        "What's in the Glow Serum and how much does it cost?"
    ]
 
    for q in queries:
        print(f"\nQ: {q}")
        print(f"A: {run_agent(q, tools, system_prompt)}")
