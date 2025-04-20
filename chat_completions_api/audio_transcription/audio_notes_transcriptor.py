import sys
from openai import OpenAI
from dotenv import load_dotenv

TRANSCRIPTION_MODEL = "gpt-4o-transcribe"


def main():
    args_count = len(sys.argv)
    if args_count < 2:
        print("Usage: python audio_notes_transcriptor.py <path-to-audio-file>")
        sys.exit(1)
    path_to_audio_file = sys.argv[1]
    audio_file = open(path_to_audio_file, "rb")
    load_dotenv()
    client = OpenAI()

    transcription = client.audio.transcriptions.create(
        model=TRANSCRIPTION_MODEL,
        file=audio_file
    )

    print(transcription.text)


if __name__ == "__main__":
    main()
