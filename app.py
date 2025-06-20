import os   # os: Used for OS-level operations
import time  # time: For introducing delay (used in typing animation).
import json  # json: For saving/loading chat history.
import streamlit as st  # streamlit: To build the web app interface.
import openai # openai, OpenAI: For calling OpenAI's API.
from openai import OpenAI 
 
# ✅ Set API key and initialize OpenAI client
# openai.api_key = "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"
openai.api_key = "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"

client = OpenAI(api_key=openai.api_key)

# ✅ Streamlit app configuration : A Streamlit app is an interactive web application built using the open-source Python library, Streamlit. Designed for data scientists, machine learning engineers, and analysts, Streamlit enables the rapid creation of data-driven web apps with minimal coding effort. It allows you to transform Python scripts into shareable web applications without requiring knowledge of front-end technologies like HTML, CSS, or JavaScript.
st.set_page_config(layout="wide", page_title="IK-Society Chatbot")
st.image("http://iksociety.org/wp-content/uploads/2020/09/logo-new.jpg", width=100)
st.title("IK-Society Chat GPT")

# ✅ Typing effect function
def type_response(response_text):      # Ye ek function hai jiska naam type_response hai. Ye ek input leta hai: response_text — yaani chatbot ka reply.
    message_placeholder = st.empty()   # Ye ek empty placeholder banata hai Streamlit me. Is jagah pe hum baad me text dikhayenge, aur bar-bar update karte rahenge jaise typing hoti hai.
 
    full_text = ""                     # full_text ek khaali string hai jisme hum complete reply gradually jodte jayenge.
    chunks = response_text.split('. ')  # Split by sentences, chunks me hum chatbot ke reply ko sentences me split kar dete hain using . (dot space) — taaki ek-ek sentence dikhaya ja sake.

    for chunk in chunks:                # Loop har sentence (chunk) ke liye chalta hai.
        if not chunk.endswith('.'):     # Agar sentence ke end me . (dot) nahi hai, toh usme dot add karte hain taaki wo complete lage.
            chunk += '.'
        full_text += chunk + " "        # Har sentence full_text me add hota jaata hai.
        message_placeholder.markdown(full_text + "▌")  # Typing cursor, ▌ ek blinking typing cursor jaisa lagta hai (cosmetic effect).
        time.sleep(0.4)                 # time.sleep(0.4) — 0.4 second ka delay har sentence ke baad, taaki typing slow aur real lage.

    message_placeholder.markdown(full_text.strip())  # Jab saare sentences type ho jaate hain, final text bina cursor ke show hota hai (clean version).
      

# ✅ Save chat to a local file
def save_chat():                 # save_chat() ek function hai jo current chat history ko local file me save karta hai.
    with open("chat_history.json", "w") as f:  # "chat_history.json" file banayi jaati hai ya overwrite hoti hai (write mode "w").
        json.dump(st.session_state.messages, f) # st.session_state.messages me Streamlit ke session ki poori chat messages stored hoti hain (user aur assistant dono ke).json.dump(...) ka use karke un messages ko JSON format me file me store kar dete hain.

# ✅ Load saved chat from file
def load_chat():                 # load_chat() function pehle se save ki gayi chat ko wapas load karta hai.
    try:                         # "chat_history.json" file ko read mode ("r") me open kiya jaata hai. 
        with open("chat_history.json", "r") as f: # Agar file mil jaati hai, toh uske andar ka JSON content wapas st.session_state.messages me daal dete hain.
            st.session_state.messages = json.load(f)
    except FileNotFoundError:
        st.session_state.messages = [{"role": "assistant", "content": "No saved chat history found."}]

# ✅ Initialize message history
if "messages" not in st.session_state:  # Ye check karta hai ki messages naam ka session variable already present hai ya nahi.
    st.session_state.messages = []      # Agar nahi hai (pehla time run ho raha hai), toh ek khaali list assign kar deta hai. st.session_state Streamlit ka ek temporary memory store hai, jo tab tak active rehta hai jab tak session khula hai.

# ✅ Sidebar controls
with st.sidebar:  # st.sidebar Streamlit ka sidebar hota hai (left side panel) with ka matlab: jitne bhi components is block ke andar likhe gaye hain, wo sab sidebar me dikhai denge.
    st.title("GPT Controls")

    if st.button("📁 Load Saved Chat"): # Sidebar me heading show hoti hai: "GPT Controls" Ye batata hai ki sidebar ka kaam kya hai — Chat control options dena.
        load_chat()                      # Jab user ye button dabata hai (📁 Load Saved Chat), toh load_chat() function call hota hai. Iska kaam hai: purani saved chat file se messages ko wapas session me load karna.

    if st.button("💾 Save Chat"):       # Jab user 💾 Save Chat button dabata hai, toh current chat ko chat_history.json file me save kar diya jaata hai using save_chat() function.
        save_chat()

    if st.button("🧹 New Chat"):    # Jab user 🧹 New Chat button dabata hai:
        st.session_state.messages = [] # st.session_state.messages ko khaali list bana diya jaata hai (yaani pura chat history reset).
        st.success("Chat cleared.")   # st.success("Chat cleared.") se ek green success message show hota hai.

# ✅ Chatbot response handler
def chatbot(messages):
    try:
        response = client.chat.completions.create(
            model="ft:gpt-3.5-turbo-0125:zubair::BXqF7b6n",
            messages=[
                {"role": "system", "content": """You are an IK-Society chatbot. When answering:
                1. Match keywords or partial questions to training data
                2. Only fetch answers from the given data, don't fetch data from web or any other external source
                3. Only use information from the training data
                4. If multiple training examples are relevant, combine them
                5. If information isn't in training data, say "I don't have that information"
                6. Provide engaging response like \' Let me know if you want more information \'
                7. Always give answers that are at least 3-4 sentences long, detailed, and engaging
                8. For unrelated questions: "I apologize, but I can only assist with questions related to IK-Society's educational institutions.\""""}
            ] + messages,
            temperature=0.3
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {str(e)}")
        return f"An error occurred: {str(e)}"

# ✅ Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ✅ Chat input and handling
prompt = st.chat_input("Ask your question about IK-Society...")
if prompt:
    # User message
    user_message = {"role": "user", "content": prompt}
    st.session_state.messages.append(user_message)

    with st.chat_message("user"):
        st.markdown(prompt)

    # Get assistant reply
    response = chatbot(st.session_state.messages)
    assistant_message = {"role": "assistant", "content": response}
    st.session_state.messages.append(assistant_message)

    with st.chat_message("assistant"):
        type_response(response)

# Old Models
# ft:gpt-3.5-turbo-0125:designlab-international::BM9jPNRS
# ft:gpt-3.5-turbo-0125:designlab-international::BMuqvM7B /- Final_Data
# ft:gpt-3.5-turbo-0125:designlab-international::BRCkUbyL /- File2804
# ft:gpt-3.5-turbo-0125:designlab-international::BRFXVuYy /- Final_Data2804