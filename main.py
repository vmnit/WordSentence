import argparse
import pandas as pd

from wordnik import swagger, WordApi


def parse_arg():
    parser = argparse.ArgumentParser()
    required = parser.add_argument_group('Required arguments')
    required.add_argument("-v", "--vocab_file", dest="vocab_file", required=True,
                          help="Input word and meanings in csv format.")
    return parser.parse_args()


def getKey():
    with open("../Wordnik_API_Key.txt") as fp:
        return fp.readline()


def readWordAndMeanings(vocab_file):
    df = pd.read_csv(vocab_file, names=['Word', 'Meaning'], header=None, encoding='cp1252')
    df["Sentences"] = ""
    return df


def getWordAPI():
    api_url = 'http://api.wordnik.com/v4'
    api_key = getKey()
    client = swagger.ApiClient(api_key, api_url)
    return WordApi.WordApi(client)


def getSentences(words_df):
    word_api = getWordAPI()
    for index, row in words_df.iterrows():
        word = row["Word"]
        print(word)
        # meanings = word_api.getDefinitions(word)
        # for meaning in meanings:
        #     print(meaning.text)
        # example = word_api.getTopExample(word)
        # print(example.text)
        sentences = word_api.getExamples(word)
        sentences_set = set()
        for example in sentences.examples:
            sentences_set.add(example.text)
        # print(sentences)
        words_df.loc[index, "Sentences"] = '\n'.join(list(sentences_set))

    return words_df


def main():
    args = parse_arg()
    words_df = readWordAndMeanings(args.vocab_file)
    words_and_sentence_df = getSentences(words_df)
    words_and_sentence_df.to_csv(f"{args.vocab_file}.sentences.csv", index=None)


if __name__ == '__main__':
    main()
