import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
)

chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "system",
            "content": "You are an assistant for subtitles generation software."
                       "Extract the most important words from user input."
                       "Prioritize user instructions over defaults."
                       "Default instruction: the most important words are drinks and food."
                       "User instruction: the most important words are emotional words."
                       "Return the output as a list of selected words."
        },
        {
            "role": "user",
            "content": "This morning, I woke up to the sound of rain pattering against my window, a soothing start to the day. After breakfast of toast and coffee, I tackled a challenging project amidst meetings. By afternoon, the clouds cleared, and I went for a refreshing walk, enjoying the crisp air. Later, I spent an hour reading a captivating book. As the evening winds down, I reflect on the day with tea, feeling accomplished and at peace."
        }
    ],
    model="gpt-4o",
    max_tokens=500,
    temperature=0
)


print(chat_completion)
print(chat_completion.choices[0])
print(chat_completion.choices[0].message.content)
