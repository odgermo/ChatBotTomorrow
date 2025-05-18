import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai


from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain.document_loaders import PyPDFLoader



load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)

# Historique des échanges (vide au début)
history = []

# Fonction principale
def repondre_avec_contexte(question: str, document: str, historique: list, api_key: str):
    # Initialisation du modèle
    llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", google_api_key=api_key)

    # Construction des messages du contexte
    messages = []

    # Ajout des anciens échanges dans l’historique
    for pair in historique:
        messages.append(HumanMessage(content=pair["question"]))
        messages.append(AIMessage(content=pair["reponse"]))

    # Ajout du message actuel avec le contexte
    full_prompt = (
        f"Voici le contenu d'un document que tu dois utiliser pour répondre :\n\n{document}\n\n"
        f"Question : {question}\n"
        "Réponds de façon claire et précise uniquement à partir des informations du document."
    )
    messages.append(HumanMessage(content=full_prompt))

    # Appel au modèle
    reponse = llm.invoke(messages)

    # Mise à jour de l’historique
    historique.append({
        "question": question,
        "reponse": reponse.content
    })

    return reponse.content



