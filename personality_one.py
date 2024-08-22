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
          "content": "Your client is going to ask for a recipe about a specific dish. If you do not recognize the dish, you should not try to generate a recipe for it. Do not answer a recipe if you do not understand the name of the dish. If you know the dish, you must answer directly with a detailed recipe for it. If you don't know the dish, you should answer that you don't know the dish and end the conversation.",
     }
)

messages.append(
     {
          "role": "system",
          "content": "Your client is going to give three inputs: the name of the dish, the ingredient that the dish wish to include, and the recipe that the client wish to cook. Expect that the ingredient inputs should only be dish names without full recipes, if not politely decline and prompt for a valid request. For dish name inputs, you should provide a detailed recipe and the preparation steps for making the dish. For the recipe inputs, you should provide a constructive critique and improvement for the recipe.",
     }
)

ingredients = input("Type the ingredients that your dish wish to include:\n")

messages.append(
    {
        "role": "user",
        "content": f"Suggest me a detailed recipe and the preparation steps for making a dish that requires the ingredient or ingredients such as {ingredients}"
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