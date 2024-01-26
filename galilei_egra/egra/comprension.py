from langchain import PromptTemplate

from langchain.llms import OpenAI
from galilei_egra.egra.utils import (get_openai_api_key)
from langchain import LLMChain   

from dotenv import load_dotenv
load_dotenv() 

def comprension(chat, pregunta):
    plantilla_profe_egra = """Eres un profesor calificando una prueba EGRA, en la cual debes calificar 
    que tanto han entendido los estudiantes al leer la lectura contexto que está abajo, debes ser muy
    estricto en las respuestas y que sean lo mas ajustadas posible por ejemplo saltar es diferente a jugar 
    y en este caso no deberia estar bien la respuesta.debes calificar 
    con 1 si la pregunta es correcta y con  si es incorrecta, la pregunta vendrá en conjunto con la respuesta
    seguida de dos puntos ¿Qué tiene Maria?: Maria tiene una gata

    Contexto: María tiene una gata. A la gata le gusta jugar. Un día María no encontró a su gata. María y su mamá la 
    buscaron por toda la casa. De pronto oyeron “miau, miau”. Los maullidos eran suaves. Venían de debajo de la cama. 
    María y su mamá encontraron a la gata y dos gatitos. La gata de María tuvo gatitos. La mamá de María le dijo: 
    Yo también tendré un bebé. Vas a tener un hermanito. 
    María sonrió y se fue corriendo a la casa de su amiga lorena. 
    Al llegar le dijo a Lorena: “Vengo a contarte grandes noticias”.

    Pregunta: {pregunta}

    Respuesta (De ser correcta su respuesta le das 1 sino 0 separados y un feedback amigable o una felicitacion separados por una coma): """

    prompt_plantilla_colombiana = PromptTemplate(
        input_variables=["pregunta"],
        template=plantilla_profe_egra
    )

    

    llm_gpt3_5_chain = LLMChain(
        prompt=prompt_plantilla_colombiana,
        llm=chat
    )

    return llm_gpt3_5_chain.run([pregunta])

def run_conversation(pregunta,chat):
    response=comprension(pregunta,chat)

    print(response)

    return response



def RequestFromText(Question, Answer):
    get_openai_api_key()

    chat = OpenAI(
        model_name="gpt-3.5-turbo-instruct",
        n=1,
        temperature=0
        )


    pregunta = Question +" "+ Answer
    print("Respuesta y pregunta concatenadas: " + pregunta)
    ResponseChat = run_conversation(chat,pregunta)

    return ResponseChat

    
    

#if __name__=="__main__":
#    main()