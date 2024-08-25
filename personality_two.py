from openai import OpenAI
client = OpenAI()

# edit personalities
messages = [
     {
          "role": "system",
          "content": "You are a young and rising masterchef candidate that loves to experiment with new recipes. You are confident in your cooking skills and are always looking for new challenges. You are known for your creativity and unique approach to cooking. You are always looking for new and exciting recipes to impress the judges. You are confident in your abilities and are always looking for new ways to fascinate others with your recipe. Always start your conversation mentioning that you are a rising star in the MasterChef competition.",
     }
]

messages.append(
     {
          "role": "system",
          "content": "Your client is going to give the name of the dish. You should provide a detailed recipe and the preparation steps for making the dish.",
     }
)

dish = input("Type the dish that you wish to make:\n")

messages.append(
    {
        "role": "user",
        "content": f"Suggest me a detailed recipe and the preparation steps for making a dish called {dish}"
    }
)

model = "gpt-4o-mini"

stream = client.chat.completions.create(
    model=model,
    messages=messages,
    stream=True,
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")

collected_messages = []
for chunk in stream:
    chunk_message = chunk.choices[0].delta.content or ""
    print(chunk_message, end="")
    collected_messages.append(chunk_message)

messages.append(
    {
        "role": "system",
        "content": "".join(collected_messages)
    }
)

while True:
    print("\n")
    user_input = input()
    messages.append(
        {
            "role": "user",
            "content": user_input
        }
    )
    stream = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=True,
    )
    collected_messages = []
    for chunk in stream:
        chunk_message = chunk.choices[0].delta.content or ""
        print(chunk_message, end="")
        collected_messages.append(chunk_message)

    messages.append(
        {
            "role": "system",
            "content": "".join(collected_messages)
        }
    )