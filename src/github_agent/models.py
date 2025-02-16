from langchain.chat_models import init_chat_model
import dotenv
from src.settings import settings

dotenv.load_dotenv()

model = init_chat_model(settings.MAIN_LLM_NAME, model_provider=settings.MAIN_LLM_PROVIDER)