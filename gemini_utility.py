import os
import json
from PIL import Image

import google.generativeai as genai

# working with directories
working_directory=os.path.dirname(os.path.abspath(__file__))

config_file_path=f"{working_directory}/config.json"
config_data= json.load(open(config_file_path))


#Loading the api key
GOOGLE_API_KEY=config_data["GOOGLE_API_KEY"]

#configuration google.generative with api key
genai.configure(api_key=GOOGLE_API_KEY)

# gemini pro model for chatbot

def load_gemini_pro_model():
    gemini_pro_model=genai.GenerativeModel("gemini-pro")
    return gemini_pro_model

# gemini pro model for image captioning

def gemini_pro_vision_response(image, prompt="given image might contain some skin disease. if it does then tell which one do you think it is otherwise say it's a healthy skin."):
    gemini_pro_vision_model=genai.GenerativeModel("gemini-pro-vision")
    image = Image.open(image)
    response=gemini_pro_vision_model.generate_content([prompt,image])
    result=response.text
    return result


# image = Image.open("samplepic.jpg")
# prompt="write a short caption for his image"
# output=gemini_pro_vision_response(prompt,image)
# print(output)