from langchain_google_genai import  ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import os, dotenv

dotenv.load_dotenv()

gemini_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash-exp")
llama_model = ChatGroq(model="llama-3.3-70b-versatile")
deepseek_model = ChatGroq(model="deepseek-r1-distill-llama-70b")