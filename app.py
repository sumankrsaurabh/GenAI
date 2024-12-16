import streamlit as st
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure API key
genai.configure(api_key=st.secrets["API_KEY"])

# Function to generate text response
def get_gemini_text_response(question):
    try:
        response = genai.chat(
            model="models/chat-bison-001",  # Verified for chat/text generation
            messages=[{"content": question}]
        )
        return response.get("candidates", [{}])[0].get("content", "No response generated.")
    except Exception as e:
        return f"Error: {e}"

# Function to generate an image
def get_gemini_image_response(prompt):
    try:
        response = genai.generate_image(
            prompt=prompt,
            model="models/imagen-3"  # Verified for image generation
        )
        return response.get("image_url", "No image URL returned.")
    except Exception as e:
        return f"Error: {e}"

# Streamlit app setup
st.set_page_config(page_title="Gemini AI Assistant", layout="wide", initial_sidebar_state="expanded")
st.title("🤖 Gemini AI Assistant")
st.markdown("**A modern app to interact with Google Gemini API for text and image generation.**")

# Sidebar for navigation
with st.sidebar:
    st.header("Navigation")
    option = st.radio(
        "Choose a feature:",
        options=["Text Generation", "Image Generation"],
        index=0
    )
    st.markdown("---")
    st.info("🔗 **Powered by Google Gemini API**")

# Text Generation UI
if option == "Text Generation":
    st.subheader("🔤 Generate Text with Gemini")
    user_input = st.text_input("Enter your text prompt:", placeholder="Ask a question or request content...")
    if st.button("Generate Text"):
        if user_input.strip():
            with st.spinner("Generating text response..."):
                response = get_gemini_text_response(user_input)
            st.markdown("### 📝 Generated Response:")
            st.write(response)
        else:
            st.warning("Please enter a valid prompt.")

# Image Generation UI
elif option == "Image Generation":
    st.subheader("🖼️ Generate Images with Imagen")
    image_prompt = st.text_input("Describe the image you want:", placeholder="e.g., A futuristic city at sunset")
    if st.button("Generate Image"):
        if image_prompt.strip():
            with st.spinner("Generating image..."):
                image_url = get_gemini_image_response(image_prompt)
                if "Error" not in image_url:
                    st.markdown("### 🌟 Generated Image:")
                    st.image(image_url, use_column_width=True, caption=image_prompt)
                else:
                    st.error(image_url)
        else:
            st.warning("Please enter a valid description.")

# Footer
st.markdown("---")
st.markdown(
    "🌟 Made with ❤️ by **Coderon** | Powered by **[Google Gemini API](https://ai.google.dev)**",
    unsafe_allow_html=True
)
