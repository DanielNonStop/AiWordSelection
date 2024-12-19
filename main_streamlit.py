import os
from openai import OpenAI
import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)

st.title("AI Word Selection")

st.sidebar.header("Input Parameters")

model = st.sidebar.selectbox("Choose a model", options=["gpt-4o-mini", "gpt-4o"])

default_instruction = \
    "You are an assistant for subtitles generation software. " \
    "Extract the most important words from user input text. " \
    "Instruction: You must select pictorial words as important words." \
    "Return the output as a list of selected words."

input_instruction = st.sidebar.text_area(
    "Input Prompt",
    default_instruction
)

# default_instruction = st.sidebar.text_area(
#     "Default instruction",
#     "You should select only drinks and food as most important words.",
#     disabled=True,
# )


temperature = st.sidebar.slider("Temperature", min_value=0.0, max_value=1.0, value=0.7, step=0.01)
max_tokens = st.sidebar.slider("Max Tokens", min_value=50, max_value=1000, value=500, step=50)

input_text = st.text_area(
    "Enter your input text",
    "This morning, I woke up to the sound of rain pattering against my window, a soothing start to the day. After breakfast of toast and coffee, I tackled a challenging project amidst meetings. By afternoon, the clouds cleared, and I went for a refreshing walk, enjoying the crisp air. Later, I spent an hour reading a captivating book. As the evening winds down, I reflect on the day with tea, feeling accomplished and at peace.",
    height=200
)

if input_instruction == '':
    input_instruction = default_instruction

# Initialize session state variables
if "history" not in st.session_state:
    st.session_state["history"] = []  # Stores the history of requests and responses

if st.button("Send Request"):
    messages = [
        {
            "role": "system",
            "content": input_instruction
        },
        {
            "role": "user",
            "content": input_text
        }
    ]

    try:
        response = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature
        )

        output = response.choices[0].message.content
        total_tokens = response.usage.total_tokens

        # Add the request and response to the history
        st.session_state["history"].append({
            "model": model,
            "input_instruction": input_instruction,
            "input_text": input_text,
            "output": output,
            "total_tokens": total_tokens,
            "temperature": temperature,
            "max_tokens": max_tokens
        })

    except Exception as e:
        st.error(f"An error occurred: {e}")

# Display the history
if st.session_state["history"]:
    st.subheader("Request History")
    for idx, entry in enumerate(reversed(st.session_state["history"])):
        st.write(f"### Request {len(st.session_state['history']) - idx}")
        st.write(f"**Model:** {entry['model']}")
        st.write(f"**Input Instruction:** {entry['input_instruction']}")
        st.write(f"**Input Text:** {entry['input_text']}")
        st.write(f"**Temperature:** {entry['temperature']}")
        st.write(f"**Max Tokens:** {entry['max_tokens']}")
        st.write(f"**Output:** {entry['output']}")
        st.write(f"**Total Tokens Used:** {entry['total_tokens']}")
        st.write("---")
