from langchain_google_genai import  ChatGoogleGenerativeAI
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv, find_dotenv

_ = load_dotenv(find_dotenv())

gemini_model = ChatGoogleGenerativeAI(model="gemini-2.0-flash")
llama_model = ChatGroq(model="llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
deepseek_model = ChatGroq(model="deepseek-r1-distill-llama-70b")