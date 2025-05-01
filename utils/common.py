from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def chamar_openai(
    user_prompt: str,
    system_message: str,
    function_def: dict = None
) -> str:
    messages = [
        { "role": "system",  "content": system_message },
        { "role": "user",    "content": user_prompt }
    ]
    kwargs = {"model": "gpt-4", "messages": messages, "temperature": 0.7}

    # se usar function calling
    if function_def:
        kwargs["functions"] = [function_def]
        kwargs["function_call"] = {"name": function_def["name"]}

    response = await client.chat.completions.acreate(**kwargs)
    return response.choices[0].message.content