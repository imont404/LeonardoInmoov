import openai
import speech_recognition as sr
#import serial
import os
import json
from vision import *
from openai import OpenAI
from pathlib import Path
from mutagen.mp3 import MP3
import time

personality = "y.txt"
openai.api_key = ""
client = OpenAI(api_key= ""
#ser = serial.Serial('COM3', 9600)

def obtener_duracion_mp3(archivo):
    audio = MP3(archivo)
    return audio.info.length

def bloquear_captura_duracion_mp3(archivo_mp3):
    duracion = obtener_duracion_mp3(archivo_mp3)
    time.sleep(duracion)

def obtener_pregunta_del_audio():
    r = sr.Recognizer()
    mic = sr.Microphone(device_index=1)
    r.dynamic_energy_threshold=False
    r.energy_threshold = 400

    # while True:
    #     start_time = time.time()
    #     bloquear_captura_duracion_mp3("output.mp3")
    with mic as source:
        print("Di algo:")
        r.adjust_for_ambient_noise(source, duration = 0.2)
        audio = r.listen(source)
        try:
            
            with open('speech.wav','wb') as f:
                f.write(audio.get_wav_data())
            with open('speech.wav', 'rb') as speech:
                wcompletion = client.audio.transcriptions.create(
                    model = "whisper-1",
                    file=speech
                )
                user_input = wcompletion.text
                print(user_input)
                # end_time = time.time()
                # print(f"Tiempo para obtener pregunta del audio: {end_time - start_time:.2f} segundos")
                return user_input
        except Exception as e:
                print(f"Error al obtener pregunta del audio: {e}")
                return None
        

def obtener_respuesta(conversacion, model="gpt-4o", temperature=0.5, max_tokens=2000):
    messages = [{"role": mensaje["role"], "content": mensaje["content"]} for mensaje in conversacion]
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature,
        max_tokens=max_tokens,
    )

    respuesta_modelo = response.choices[0].message.content
    voz_leonardo(respuesta_modelo)
    #ser.write(b'1') 
    # end_time = time.time()  # Tiempo final
    # print(f"Tiempo para obtener respuesta: {end_time - start_time:.2f} segundos")
    return respuesta_modelo

def guardar_feedback(feedback):
    filename = f"feedback_{1}.txt"

    with open(filename, 'w') as file:
        file.write(feedback)

    print(f"Feedback guardado en {filename}")

def voz_leonardo(respuesta_modelo, nombre_archivo="output.mp3"):
  #  speech_file_path = Path(__file__).parent / nombre_archivo
    response = client.audio.speech.create(
        model="tts-1",
        voice="onyx",
        input=respuesta_modelo
    )
    response.stream_to_file("output.mp3") #no se porque lo tacha pero sirve asi que no se toca

    if os.path.isfile("output.mp3"):
        os.startfile("output.mp3")

# Inicio de la conversación
def its_alive():
    with open(personality, "r") as file:
        mode = file.read()

    conversacion = [
        {"role": "user", "content": f"{mode}"},
        {"role": "assistant", "content": "Entendido"}
    ]


    feedback_solicitado = False

    while True:
        
        pregunta = obtener_pregunta_del_audio()

        if pregunta:
            conversacion.append({"role": "user", "content": pregunta})

            #feedback
            if "i want to give some feedback" in pregunta.lower():
                feedback_solicitado = True
                respuesta_feedback = (
                    "Of course, I'm all ears! Feel free to share your feedback, and I'll do my best to assist you. And don't worry, I won't take it too hard, I promise!"
                )
                #ser.write(b'1')
                voz_leonardo(respuesta_feedback)
                #ser.write(b'0')
            elif "grab this" in pregunta.lower():
                #ser.write(b'1')
                respuesta_agarrar = (
                    "Of course"
                )
                
                voz_leonardo(respuesta_agarrar)
        
            elif "describe what you're seeing" in pregunta.lower():
                descripcion = describe_image(openai.api_key)
                conversacion.append({"role": "system", "content": f"Descripción de la imagen: {descripcion}"})
                voz_leonardo(descripcion)

            elif "go to sleep" in pregunta.lower():
                break


            else:
                respuesta = obtener_respuesta(conversacion)
                print("Respuesta:", respuesta)
                #ser.write(b'0')
                conversacion.append({"role": "assistant", "content": respuesta})

        if feedback_solicitado:
            print("Por favor, proporciona tu feedback:")
            feedback_usuario = obtener_pregunta_del_audio()

            if feedback_usuario:
                guardar_feedback(feedback_usuario)
                feedback_solicitado = False
        else:
            print("...")

its_alive()
