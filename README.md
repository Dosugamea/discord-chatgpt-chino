## Discord ChatGPT-Chino

Bring your Discord server to life with ChatGPT-Chino

This is a simple chatbot for Discord that uses OpenAI's GPT model for generating text-based responses and VV for generating audio responses. The bot can join and leave voice channels and play audio responses based on the generated text.

### Setup

- Clone the repository and navigate into the project directory.
- Create a virtual environment and install the dependencies:

```
poetry install
```

- Create a file named .env in the project directory and add the following lines:

```
CHATGPT_API_KEY=<your_chatgpt_api_key>
DISCORD_BOT_TOKEN=<your_bot_token>
VV_API_KEY=<your_vv_api_key>
VV_SPEAKER_ID=<your_vv_speaker_id>
VV_ENDPOINT_QUERY="http://127.0.0.1:50031/audio_query"
VV_ENDPOINT_SPEAKER="http://127.0.0.1:50031/speakers"
VV_ENDPOINT_AUDIO="http://127.0.0.1:50031/synthesis"
```

Replace <your_chatgpt_api_key>, <your_bot_token>, <your_vv_api_key>, and <your_vv_speaker_id> with your actual values. You can obtain a Discord bot token from the Discord Developer Portal. To obtain a ChatGPT API key, you can refer [ChatGPT website](https://openai.com/).

- Run the bot:

```
poetry run python src/main.py
```

### Usage

The bot responds to the following commands:

- !chat <prompt>: Generates a text-based response based on the given prompt and sends it to the chat. If the bot is currently in a voice channel, it will also generate an audio response based on the text and play it in the channel.
- !join: Joins the voice channel that the user is currently in.
- !leave: Leaves the voice channel.

### License

This project is licensed under the AGPLv3 License. See the LICENSE file for details.

### Contributors

- Dosugamea
- ChatGPT-kun
  - Almost codes are stolen directly from ChatGPT-kun, thanks a lot!
