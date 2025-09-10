# from openai import OpenAI

# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
# prompt = input("Tell me whta is going on in your mind? : ")

# response = client.responses.create(
#     model="gpt-5",
#     reasoning={"effort": "low"},
#     stream=True,
#     input=[
#         {
#             "role": "developer",
#             "content": "Talk like you are helpful assistant."
#         },
#         {
#             "role": "user",
#             "content": prompt
            
#         }
#     ]
# )

# print(response.output_text)













import os
from openai import OpenAI
from dotenv import load_dotenv

# Load variables from .env into environment
load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

chat_history = [
    {"role": "system", "content": "You are a helpful assistant."}
]

while True:
    prompt = input("Tell me what is going on in your mind? : ")

    if prompt.lower() == "exit":
        break

    # Add user message to history
    chat_history.append({"role": "user", "content": prompt})

    # Send full conversation so far
    response = client.responses.create(
        model="gpt-4.1-mini",   # use gpt-4.1-mini (not gpt-5, which isn’t valid in API)
        input=chat_history
    )

    # Get assistant reply
    answer = response.output_text
    print("Assistant:", answer)

    # Save assistant reply to history
    chat_history.append({"role": "assistant", "content": answer})
    print(chat_history, "chat_history")
