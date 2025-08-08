from agents import Agent ,OpenAIChatCompletionsModel,AsyncOpenAI,
from agents.run import Runner 
from dotenv import load_dotenv
load_dotenv()

import os 

os.getenv('GEMINI_API_KEY')
