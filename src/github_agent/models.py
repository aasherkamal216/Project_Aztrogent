from langchain.chat_models import init_chat_model
import os, dotenv

dotenv.load_dotenv()

gemini_model = init_chat_model("gemini-2.0-flash-exp", model_provider="google_genai")