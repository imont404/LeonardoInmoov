from openai import OpenAI
client = OpenAI(api_key= "")

response = client.audio.speech.create(
    model="tts-1",
    voice="onyx",
    input="Hello, my name is Leonardo prueba",
)

response.stream_to_file("output.mp3")