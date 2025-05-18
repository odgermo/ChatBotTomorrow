import streamlit as st
import os
from dotenv import load_dotenv
import google.generativeai as genai
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain.document_loaders import PyPDFLoader
from file import repondre_avec_contexte
import tempfile


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=api_key)
# Historique des échanges (vide au début)
history = []




#INTERFACE STREAMLIT

st.set_page_config(page_title="Chatbot PDF Dossier", layout="centered")
st.title("🤖 Chatbot PDF pour Dossier d'Appel d'Offre")

# API Key
api_key = api_key

# Uploader le dossier contenant des PDF
uploaded_files = st.file_uploader("📁 Téléversez un dossier contenant des fichiers PDF", type=["pdf"], accept_multiple_files=True)

# Créer une variable d'état pour stocker les textes des PDF et l'historique
if "pdf_text" not in st.session_state:
    st.session_state.pdf_text = ""
if "history" not in st.session_state:
    st.session_state.history = []

# Lecture des fichiers PDF
if uploaded_files:
    texts = []
    for uploaded_file in uploaded_files:
        # Stockage temporaire
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.read())
            tmp_path = tmp_file.name
        # Extraction du texte
        loader = PyPDFLoader(tmp_path)
        docs = loader.load()
        pdf_text = "\n".join([doc.page_content for doc in docs])
        texts.append(pdf_text)
        os.unlink(tmp_path)  # Nettoyage

    # Stocker tout le contenu
    st.session_state.pdf_text = "\n\n".join(texts)
    st.success("✅ Fichiers PDF chargés avec succès !")

# Zone de saisie de la question
if st.session_state.pdf_text and api_key:
    question = st.text_input("💬 Posez votre question :", key="question_input")

    if st.button("📤 Envoyer la question") and question.strip():
        reponse = repondre_avec_contexte(
            question=question,
            document=st.session_state.pdf_text,
            historique=st.session_state.history,
            api_key=api_key
        )
        st.markdown("### 🤖 Réponse :")
        st.write(reponse)

        # Affichage de l'historique
        with st.expander("🕒 Voir l'historique des échanges"):
            for i, pair in enumerate(st.session_state.history):
                st.markdown(f"**Q{i+1} :** {pair['question']}")
                st.markdown(f"**R{i+1} :** {pair['reponse']}")
else:
    st.info("📝 Veuillez téléverser des fichiers PDF et entrer votre clé API.")