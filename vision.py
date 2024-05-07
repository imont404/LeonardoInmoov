import base64
import requests
import cv2
from PIL import Image

api_key = ""

def capture_image():
  cap = cv2.VideoCapture(0)
  if not cap.isOpened():
    print("No se puede abrir la cámara")
    return None

  ret, frame = cap.read()
  if not ret:
    print("No se puede capturar la imagen de la cámara")
    return None

  image_path = "captura.jpeg"
  cv2.imwrite(image_path, frame)
    
  cap.release()
  cv2.destroyAllWindows()
    
  return image_path

def encode_image(image_path):
  with open(image_path, "rb") as image_file:
    return base64.b64encode(image_file.read()).decode('utf-8')

def describe_image(api_key):
  image_path = capture_image()
  if image_path is not None:

    base64_image = encode_image(image_path)

    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {api_key}"
    }

    payload = {
      "model": "gpt-4-vision-preview",
      "messages": [
        {
          "role": "user",
          "content": [
            {
              "type": "text",
              "text": "Whats in this image?"
            },
            {
              "type": "image_url",
              "image_url": {
                "url": f"data:image/jpeg;base64,{base64_image}"
              }
            }
          ]
        }
      ],
      "max_tokens": 300
    }

    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    #print(response.json())
    try:
        response_data = response.json()
        descriptions = response_data.get("choices", [{}])[0].get("message", {}).get("content", "No description provided.")
        print(descriptions)
        return descriptions
    except Exception as e:
        return str(e)
    