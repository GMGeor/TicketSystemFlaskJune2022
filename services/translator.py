from decouple import config
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import LanguageTranslatorV3


class TranslateService:
    def __init__(self):
        apikey = config("TRANSLATOR_API_KEY")
        url = config("TRANSLATOR_URL")
        version = config("TRANSLATOR_VERSION")
        authenticator = IAMAuthenticator(apikey)
        self.language_translator = LanguageTranslatorV3(
            version=version, authenticator=authenticator
        )
        self.language_translator.set_service_url(url)

    def identify_lang(self, language_translator, text):
        language_detection = language_translator.identify(text).get_result()
        max_confidence = 0
        identified_lang = ""
        for lang in language_detection["languages"]:
            current_confidence = lang["confidence"]
            if current_confidence > max_confidence:
                max_confidence = current_confidence
                identified_lang = lang["language"]
        return identified_lang

    def translate(self, text, translate_to):
        try:
            translate_from = self.identify_lang(self.language_translator, text)
            if not translate_from == translate_to:
                model_id = translate_from + "-" + translate_to
                translation = self.language_translator.translate(
                    text=text, model_id=model_id
                ).get_result()
                return translation["translations"][0]["translation"]
        except Exception as ex:
            raise Exception(ex)
