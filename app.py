import streamlit as st
import asyncio
from agents import Runner


from socialmedia_media_agent import content_writer_agent, get_transcript

st.set_page_config(
    page_title="Social Media Content Generator",
    page_icon="📱",
    layout="wide",
)

st.title("Social Media Content Generator")
st.markdown("""
This app generates social media content based on YouTube video transcripts.
Enter a Youtube video ID and your query to generate content for different platforms.""")

st.header("Input")
col1, col2 = st.columns(2)

with col1:
    video_id = st.text_input("Youtube video id", placeholder="e.g., hTWKbfoikeg")
    st.caption("The ID is the part after 'v=' in a youtube URL.")

with col2:
    query = st.text_area(
        "Your Query (Optional)",
        placeholder="e.g., Generate a Linkedin post and an Instagram caption based on this video",
        height=100,
    )

st.subheader("Select platforms")
col1, col2, col3 = st.columns(3)

with col1:
    linkedin = st.checkbox("LinkedIn", value=True)
with col2:
    instagram = st.checkbox("Instagram", value=True)
with col3:
    twitter = st.checkbox("Twitter", value=True)

async def run_agent(vid_id, user_query, platforms):
    try:
        transcript = get_transcript(vid_id)
        if not transcript:
            return None, "Nie udało się pobrać transkrypcji z tego filmu. Sprawdź ID."

        platforms_str = " and ".join(platforms)
        msg = f"Generate a {platforms_str} post based on this transcript: {transcript}"
        if user_query:
            msg = f"{user_query} for {platforms_str} based on this video transcript: {transcript}"
        

        result = await Runner.run(content_writer_agent, input=msg)
        return result, None
    except Exception as e:
        return None, str(e)


if st.button("Generate Content", type="primary", disabled=not video_id):
    selected_platforms = []
    if linkedin:
        selected_platforms.append("LinkedIn")
    if instagram:
        selected_platforms.append("Instagram")
    if twitter:
        selected_platforms.append("Twitter")

    if not selected_platforms:
        st.error("Please select at least one social media platform")
    else:
        with st.spinner("Generating content... This may take a minute."):
            result, error = asyncio.run(run_agent(video_id, query, selected_platforms))

            if error:
                st.error(f"Error: {error}")
            elif result and result.final_output:
                st.header("Generated Content")
                

                content = result.final_output
                st.markdown(content)
                
                st.download_button(
                    label="Download Content as TXT",
                    data=content,
                    file_name="social_media_posts.txt",
                    mime="text/plain"
                )
            else:
                st.error("Brak wyniku. Agent mógł odmówić działania.")

st.markdown("---")
st.caption("Powered by GROQ and YouTube Transcript API")