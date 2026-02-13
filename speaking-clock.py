from dotenv import load_dotenv
from datetime import datetime
import os

# Import namespaces
from azure.core.credentials import AzureKeyCredential
import azure.cognitiveservices.speech as speech_sdk


def main():

    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        global speech_config

        # Get config settings
        load_dotenv()
        speech_key = os.getenv('SPEECH_KEY')
        speech_region = os.getenv('SPEECH_REGION')

        # Configure speech service
        speech_config = speech_sdk.SpeechConfig(speech_key, speech_region)
        print("Ready to use speech service in:", speech_config.region)

        # Get spoken input
        command = TranscribeCommand()

        if command.lower() == "what time is it?":
            TellTime()
        else:
            print("Command not recognized:", command)

    except Exception as ex:
        print("Error:", ex)


def TranscribeCommand():
    command = ""

    # Configure speech recognition
    current_dir = os.getcwd()
    audioFile = current_dir + "/time.wav"

    audio_config = speech_sdk.AudioConfig(filename=audioFile)
    speech_recognizer = speech_sdk.SpeechRecognizer(
        speech_config=speech_config,
        audio_config=audio_config
    )

    # Process speech input
    print("Listening...")
    speech = speech_recognizer.recognize_once_async().get()

    if speech.reason == speech_sdk.ResultReason.RecognizedSpeech:
        command = speech.text
        print("You said:", command)

    else:
        print("Speech not recognized:", speech.reason)

        if speech.reason == speech_sdk.ResultReason.Canceled:
            cancellation = speech.cancellation_details
            print("Canceled:", cancellation.reason)
            print("Error details:", cancellation.error_details)

    # Return the command
    return command


def TellTime():
    now = datetime.now()
    response_text = "The time is {}:{:02d}".format(now.hour, now.minute)

    # Configure speech synthesis
    output_file = "output.wav"

    speech_config.speech_synthesis_voice_name = "en-GB-RyanNeural"
    audio_config = speech_sdk.audio.AudioConfig(filename=output_file)

    speech_synthesizer = speech_sdk.SpeechSynthesizer(
        speech_config=speech_config,
        audio_config=audio_config
    )

    # Synthesize spoken output
    speak = speech_synthesizer.speak_text_async(response_text).get()

    if speak.reason == speech_sdk.ResultReason.SynthesizingAudioCompleted:
        print("Spoken output saved in", output_file)
    else:
        print("Speech synthesis failed:", speak.reason)

    # Print the response
    print(response_text)


if __name__ == "__main__":
    main()
