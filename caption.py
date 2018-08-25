import random
import json

from joblib import Parallel, delayed

from googletrans import Translator

from textblob import TextBlob
from textblob import Word

TRANSLATOR = Translator()

CAPTIONS = [
    "A green dog plays on the grass.",
    "A clown stands on the table.",
    "Two balls roll down a hill.",
    "A snowman stands between two cats."

]

LANGUAGES = [
    ["ar", "en"],  # arabic
    ["hy", "en"],  # armenian
    ["el", "en"],  # greek
    ["eu", "en"],  # basque

    ["el", "eu", "en"],
    ["hy", "ar", "en"],
]


def augment_translate_trans(captions, languages):
    for ln in languages:
        captions = TRANSLATOR.translate(captions, dest=ln)
        captions = [caption.text for caption in captions]

    return captions


def augment_translate_blob(id, comment, languages):
    if hasattr(comment, "decode"):
        comment = comment.decode("utf-8")

    text = TextBlob(comment)
    for language in languages:
        text = text.translate(to=language)

    return id, languages, str(text)


def augment_synonym(line):
    # TODO make work
    words = line.split(" ")
    output = list()
    for word_str in words:
        word_obj = Word(word_str)
        if len(word_str) > 3 and len(word_obj.synsets) > 0:
            random_synset = random.choice(word_obj.synsets)
            random_lemma = random.choice(random_synset.lemma_names())
            output.append(random_lemma.replace('_', ' '))
        else:
            output.append(word_str)
    return " ".join(output)


def augment_hypernym(line):
    # TODO make work
    words = line.split(" ")
    output = list()
    for word_str in words:
        word_obj = Word(word_str)
        if len(word_str) > 3 and len(word_obj.synsets) > 0:
            random_synset = random.choice(word_obj.synsets)

            if len(random_synset.hypernyms()) > 0:
                random_synset = random.choice(random_synset.hypernyms())

            random_lemma = random.choice(random_synset.lemma_names())
            output.append(random_lemma.replace('_', ' '))
        else:
            output.append(word_str)
    return " ".join(output)

#TODO add spell checking
#TODO add grammar checking (gramar score -> choose best translation?)

def main_tmp():
    for lan in LANGUAGES:
        res = augment_translate_trans(CAPTIONS, lan)
        print(res)

def main():
    with open('data/pretty_train.json') as in_file:
        data = {"annotations": json.load(in_file)["annotations"]}

        languages = ["el", "eu", "en"]
        annotations = data["annotations"][:10]
        print(annotations)

        parallel = Parallel(300, backend="threading", verbose=5)
        translated_data = parallel(delayed(augment_translate_blob)(comment["id"], comment["caption"], languages) for comment in annotations)

        train_data = {
            "annotations": translated_data
        }

        with open('data/captions_train2014_test.json', "w") as out_file:
            json.dump(train_data, out_file)

if __name__ == "__main__":
    main_tmp()
    #main()
