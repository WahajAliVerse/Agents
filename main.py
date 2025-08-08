from agents import Agent ,enable_verbose_stdout_logging,OpenAIChatCompletionsModel,AsyncOpenAI,RunConfig
from agents.run import Runner 
from dotenv import load_dotenv
load_dotenv()
import asyncio
import os 
import chainlit as cl


# enable_verbose_stdout_logging()
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

client = AsyncOpenAI(
    api_key=GEMINI_API_KEY,
   base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model='gemini-2.0-flash',
    openai_client=client
)

config = RunConfig(
    model_provider=client,
    model=model,
    tracing_disabled=True
)


Tutor_Agent = Agent(
    name='Tutor Agent',
    instructions=""" You're a helpful tutor for a students you answer students queries helping students understand concepts.""",
model=model
)

Technical_support_Agent = Agent(
    name='Technical support Agent',
    instructions=""" You're a helpful techincal support agent for a students you answer students queries helping students understand concepts and solve their problems.""",
model=model
)

Triage_Agent = Agent(
    name='Triage Agent',
    instructions=""" You're a helpful triage agent for all agents you should read user query decide which agent resolve student query is you know hows solve user query u can handle it by yourself.""",
model=model,
handoffs=[Technical_support_Agent,Tutor_Agent],

)

async def main():
    prompt = str(input("How may i help you?"))

    result = Runner.run_streamed(Triage_Agent,prompt,run_config=config)
    async for e in result.stream_events():
        if e.type == 'raw_response_event' and hasattr(e.data, 'delta'):
            print(e.data.delta,end='',flush=True)
    print('Handsoff Agents',result.last_agent)
    # print(result.final_output)



if __name__ == '__main__':
    asyncio.run(main())