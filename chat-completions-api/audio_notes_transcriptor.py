from openai import OpenAI
from dotenv import load_dotenv

def main():
    load_dotenv()
    client = OpenAI()

    completion = client.chat.completions.create(
        model="o4-mini",
        messages=[
            {
                "role": "user",
                "content": "Say hello to my new Python Open AI playground."
            }
        ]
    )

    print(completion.choices[0].message.content)


if __name__ == "__main__":
    main()
