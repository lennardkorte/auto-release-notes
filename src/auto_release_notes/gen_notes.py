from litellm import completion

def generate(changes: str, prompt: str, model: str, apikey: str) -> str:
    response = completion(
        model=model,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": changes}
        ],
        api_key=apikey,
        api_version="v1",
    )

    return response["choices"][0]["message"]["content"]