from spellchecker import SpellChecker
import language_check


def main():
    candidates = [
        'something iS Hapenning here',
        'this is ery bAd',
        'a gren cat is moning',
    ]

    for c in candidates:
        print("Caption: '{}' Spell Error Rate: {}".format(c, spell_error_rate(c)))
        print("Caption: '{}' Language Error Rate: {}".format(c, language_error_rate(c)))
        print("Caption: '{}' Total Error Rate: {}".format(c, total_error_rate(c)))

def total_error_rate(caption):
    er_0 = spell_error_rate(caption)
    er_1 = language_error_rate(caption)

    return (er_0 + er_1) / 2

def spell_error_rate(caption):
    words = caption.lower().split()
    spell = SpellChecker()
    misspelled = spell.unknown(words)

    return (len(misspelled) / len(words))

def language_error_rate(caption):
    caption = caption.lower()
    tool = language_check.LanguageTool('en-US')
    matches = tool.check(caption)

    return len(matches) / len(caption.split())

if __name__ == "__main__":
    main()
 
