from openai import OpenAI
from consts import APIKEYOAI

client = OpenAI(api_key=APIKEYOAI)
from consts import APIKEYOAI

def new_ai_post(titulo,extracto_texto):

    print ("Se inicio correctamente la función new_ai_post")

    if titulo:
        print ("Se recibio el valor del titulo")

    if extracto_texto:
        print ("Se recivio el valor del extrato de texto")

    # Establecer la clave de API de OpenAI


    prompt = f"Crea un articulo original optimizado para SEO con esta información: {titulo} {extracto_texto}"

    # Configurar el modelo de lenguaje
    modelo = "gpt-3.5-turbo"
    mensaje = [
        {"role":"system","content":"Eres un experto en redacción de articulos."},
        {"role":"user","content":prompt}
    ] 

    # Generar la respuesta utilizando la API de OpenAI
    response = client.chat.completions.create(model=modelo,
    messages=mensaje,
    temperature=0.8,
    max_tokens=1024)

    respuesta = response.choices[0].message.content

    return respuesta
