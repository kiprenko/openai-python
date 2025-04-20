import sys
from openai import OpenAI
from dotenv import load_dotenv


TRANSCRIPTION_MODEL = "gpt-4o-transcribe"
STRUCTURE_MODEL = "gpt-4.1"


def main():
    args_count = len(sys.argv)
    if args_count < 2:
        print("Usage: python audio_notes_transcriptor.py <path-to-audio-file>")
        sys.exit(1)
    load_dotenv()
    path_to_audio_file = sys.argv[1]
    audio_file = open(path_to_audio_file, "rb")
    client = OpenAI()

    transcription = transcript(client, audio_file)
    structured_transcription = structure(client, transcription.text)

    print(structured_transcription)


def transcript(client, audio_file):
    return client.audio.transcriptions.create(
        model=TRANSCRIPTION_MODEL,
        file=audio_file
    )

def structure(client, transcription):
    return client.chat.completions.create(
    model=STRUCTURE_MODEL,
    messages=[
        {
            "role": "system",
            "content": "Your task is to structure and organise transcriptions of audio notes. "
                       "You accept a transcription and provide the structured version of it in the same language. "
                       "Do not use Markdown, emoji or any other text formatting. "
                       "Make the text laconic and easy to read, get rid of any vermin words. "
                       "The result must look like "
                       "a title and a paragraph with the summary of the given audio note transcription."
        },
        {
            "role": "user",
            "content": transcription
        }
    ]
    ).choices[0].message.content


if __name__ == "__main__":
    main()
