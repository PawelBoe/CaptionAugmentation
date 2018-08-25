from google.cloud import translate


def main():
    translate_client = translate.Client()

    text = u'Hello, world!'
    target = 'ru'

    translation = translate_client.translate(
        text,
        target_language=target)

    print(u'Text: {}'.format(text))
    print(u'Translation: {}'.format(translation['translatedText']))

if __name__ == "__main__":
    main()
