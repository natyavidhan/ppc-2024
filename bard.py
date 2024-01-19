# from dotenv import load_dotenv
# import os
# from bardapi import Bard


# load_dotenv()

# # Replace "YOUR_API_KEY" with the actual API Key obtained earlier
# API_KEY = os.getenv("API_KEY")

# bard = Bard()
# bard.get_answer("hello")['content']

key="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"

import openai 
openai.api_key = key
messages = [ {"role": "system", "content": "You are a intelligent assistant."} ] 
while True: 
    message = input("User : ") 
    if message: 
        messages.append( 
            {"role": "user", "content": message}, 
        ) 
        chat = openai.ChatCompletion.create( 
            model="gpt-3.5-turbo", messages=messages 
        ) 
    reply = chat.choices[0].message.content 
    print(f"ChatGPT: {reply}") 
    messages.append({"role": "assistant", "content": reply}) 