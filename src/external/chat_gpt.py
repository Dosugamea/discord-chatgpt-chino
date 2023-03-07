import aiohttp


async def get_chatgpt_response(message: str, api_key: str) -> str:
    url = "https://api.openai.com/v1/engine/davinci-codex/completions"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {api_key}",
    }
    data = {"prompt": message, "max_tokens": 60, "n": 1, "stop": "\n"}
    async with aiohttp.ClientSession() as session:
        async with session.post(url, headers=headers, json=data) as response:
            response_text = (await response.json())["choices"][0]["text"]
            return response_text
