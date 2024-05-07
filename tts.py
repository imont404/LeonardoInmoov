from openai import OpenAI
client = OpenAI(api_key= "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")

response = client.audio.speech.create(
    model="tts-1",
    voice="onyx",
    input="Hello, my name is Leonardo prueba",
)

response.stream_to_file("output.mp3")