import os
import streamlit as st
from dotenv import load_dotenv
from PIL import Image
from google import genai

# 1. Initialization
load_dotenv()
client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

# 2. Function to get Gemini Response
def get_gemini_response(input_prompt, image_data):
    # We use the updated 'gemini-2.5-flash' for speed and multimodal accuracy
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[input_prompt, image_data]
    )
    return response.text

# 3. Streamlit UI Setup
st.set_page_config(page_title="AutoSage: Vehicle Expert", page_icon="🏍️")
st.header("AutoSage - AI Vehicle Specialist")

uploaded_file = st.file_uploader("Upload an image of a motorcycle or car...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Specimen", use_container_width=True)

input_prompt = """
You are an expert automotive consultant. Analyze the provided image of the vehicle and:
1. Identify the Brand and Model.
2. List key technical specifications (Engine, Power, Torque).
3. Estimate Mileage and Price range (if applicable).
4. Provide a brief 'Pros & Cons' review for a potential buyer.
5. Suggest maintenance tips or eco-friendly alternatives if relevant.
"""

submit = st.button("Analyze Vehicle")

# 4. Logic Execution
if submit:
    if uploaded_file is not None:
        with st.spinner('AutoSage is analyzing the vehicle...'):
            response = get_gemini_response(input_prompt, image)
            st.subheader("AutoSage Expert Analysis")
            st.write(response)
    else:
        st.warning("Please upload an image first!")