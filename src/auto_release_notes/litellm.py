import os
from litellm import completion

def generate():
    # Set the API key in the environment variable or directly in config
    os.environ["GEMINI_API_KEY"] = os.environ.get("GEMINI_API_KEY") or "your-key-here"

    response = completion(
        model="gemini/gemini-2.0-flash-latest",  # Adjust model name as needed
        messages=[
            {"role": "user", "content": "INSERT_INPUT_HERE"}
        ],
        api_base="https://generativelanguage.googleapis.com/v1beta",
        api_key=os.environ["GEMINI_API_KEY"],
        stream=True
    )

    for chunk in response:
        if "choices" in chunk and chunk["choices"]:
            print(chunk["choices"][0]["delta"].get("content", ""), end="")