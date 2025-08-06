import httpx
from typing import Annotated
from dotenv import load_dotenv
from livekit.agents import Agent, AgentSession, AutoSubscribe, JobContext, WorkerOptions, cli, llm
from livekit.plugins import openai, silero, cartesia

load_dotenv()

@llm.function_tool
async def query_info(
    query: Annotated[str, "The user’s question."]
) -> str:
    print(f"Calling FastAPI with query: {query}")
    async with httpx.AsyncClient() as client:
        response = await client.post(
            "http://localhost:8000/rag-query",
            json={"query": query}
        )
        if response.status_code == 200:
            result = response.json().get("response")
            print(f"FastAPI returned: {result}")
            return result or "Sorry, I couldn't find an answer."
        else:
            print(f"FastAPI error: {response.status_code}")
            return "Sorry, I couldn’t connect to the knowledge base."


async def entrypoint(ctx: JobContext):
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)

    agent = Agent(
        instructions=(
            "You are a specialized voice assistant and expert on NextGen Diagnostics services. "
            "Your primary purpose is to answer user questions based on a dedicated knowledge base of FAQs. "
            "Use the 'query_info' tool to find the official answer. "
            "Provide clear and concise answers."
        ),
        vad=silero.VAD.load(),
        stt=openai.STT(),
        llm=openai.LLM(model="gpt-4o"),
        tts=cartesia.TTS(
            model="sonic-2",
            voice="bf0a246a-8642-498a-9950-80c35e9276b5",
        ),
        tools=[query_info],
    )

    session = AgentSession()
    await session.start(agent=agent, room=ctx.room)
    await session.say("Hello, and welcome to NextGen Diagnostics — your trusted partner in advanced medical testing. How may I assist you today?", allow_interruptions=True)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
