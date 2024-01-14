import asyncio
from google.oauth2 import service_account
from google.cloud import texttospeech
from speechgenerator import SpeechGenerator, SpeechGeneratorLang


class GoogleSpeechGenerator(SpeechGenerator):

    def __init__(self):
        credentials = service_account.Credentials.from_service_account_file('speechgenerator/keyfile.json')
        self.client = texttospeech.TextToSpeechAsyncClient(credentials=credentials)

    async def text_to_speech(self, text: str, lang: SpeechGeneratorLang):
        synthesis_input = texttospeech.SynthesisInput(
            text=text
        )
        voice = texttospeech.VoiceSelectionParams(
            language_code=lang,
            ssml_gender=texttospeech.SsmlVoiceGender.FEMALE,
        )
        audio_config = texttospeech.AudioConfig(
            audio_encoding=texttospeech.AudioEncoding.OGG_OPUS
        )
        response = await self.client.synthesize_speech(
            input=synthesis_input,
            voice=voice,
            audio_config=audio_config
        )

        with open("out.ogg", "wb") as f:
            f.write(response.audio_content)
