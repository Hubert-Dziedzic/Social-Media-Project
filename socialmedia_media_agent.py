import asyncio
import os
from youtube_transcript_api import YouTubeTranscriptApi

# Important imports from openai-agents
from agents import (
    Agent, 
    Runner, 
    set_default_openai_client, 
    set_default_openai_api,
    set_tracing_disabled
)
from openai import AsyncOpenAI
from dotenv import load_dotenv

load_dotenv()

# Groq API settings
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

# Create asynchronous client
groq_async_client = AsyncOpenAI(api_key=GROQ_API_KEY, base_url=GROQ_BASE_URL)

# Library configuration
set_default_openai_client(groq_async_client, use_for_tracing=False)
set_default_openai_api("chat_completions")
set_tracing_disabled(True)

# Simple agent - returns text only
content_writer_agent = Agent(
    name="Content Writer Agent",
    instructions="""You are a talented content writer who writes engaging, humorous, highly readable social media posts.
    You will be given a video transcript and social media platforms.
    You will generate a social media post based on the video transcript and the social media platforms.
    Format the output clearly with the platform name at the top.""",
    model="llama-3.3-70b-versatile"
)

def get_transcript(video_id: str, languages: list = None) -> str:
    if languages is None:
        languages = ["en", "pl"]
    try:
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.list(video_id)
        transcript = transcript_list.find_transcript(languages)
        fetched_transcript = transcript.fetch()
        
        transcript_text = " ".join(snippet.text for snippet in fetched_transcript)
        return transcript_text
        
    except Exception as e:
        print(f"Error fetching transcript: {e}")
        return ""

async def main():
    video_id = "Szox9wD4HRU" # Sample ID
    transcript = get_transcript(video_id)
    
    if not transcript:
        print("Failed to fetch transcript. Check the video ID.")
        return
        
    input_text = f"Platform: Twitter. Transcript: {transcript}"
    
    print("Agent is starting to work (this may take a moment)...")
    
    # Run the agent
    result = await Runner.run(content_writer_agent, input=input_text)
    
    print("\n--- GENERATED POSTS ---")
    
    if result.final_output:
        print(result.final_output)
    else:
        print("No result. The agent might have refused to act.")

if __name__ == "__main__":
    asyncio.run(main())