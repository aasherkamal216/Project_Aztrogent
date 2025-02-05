"""Utility & helper functions."""

from langchain.chat_models import init_chat_model
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import BaseMessage
import os, dotenv

dotenv.load_dotenv()

