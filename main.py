import string
import nltk
from nltk import FreqDist
import pandas as pd
from colorama import Fore

vocabulary_count = 478;


# preprocessing stage to remove punctuations
def preprocessingstage(comment):
    comment = "".join(char for char in comment if char not in string.punctuation)
    comment = comment.strip()
    comment = "<" + comment + ">"
    tokens = nltk.word_tokenize(comment.lower())
    return tokens


# smoothing
def one_smoothing_stage(count_w, count_h):
    v = vocabulary_count
    return (count_w+1) / (count_h+v)


def probability_calculation(bigramfrequency, unigramfrequency, bigramsofcomment):
    probability = 1.0
    for x in range(len(bigramsofcomment)):
        if bigramsofcomment[x] in bigramfrequency:
            count_w = bigramfrequency[bigramsOfComment[x]]
        else:
            count_w = 0

        if bigramsofcomment[x][0] in unigramfrequency:
            count_h = unigramfrequency[bigramsofcomment[x][0]]
        else:
            count_h = 0

        probability = probability * one_smoothing_stage(count_w,count_h)
    return probability


def probabiliy(bigramsofcomment, corpus):
    unigrams = []
    bigrams = []

    for line in corpus:
        tokens = preprocessingstage(line)
        unigrams = unigrams + list(tokens)
        bigram = nltk.bigrams(tokens)
        bigrams = bigrams + list(bigram)

    unigramFrequency = FreqDist(unigrams)
    bigramFrequency = FreqDist(bigrams)
    print(bigramFrequency.items())

    probabiliy = probability_calculation(bigramFrequency, unigramFrequency,bigramsofcomment)
    return probabiliy


def perplexity(probability, n):
    return pow(probability, (-1/n))


if __name__ == '__main__':

    df = pd.read_excel("comments.xlsx")

    negative_df = df[df["ANNOTATION"] == "Negative"]
    negComments = negative_df["COMMENT"]

    positive_df = df[df["ANNOTATION"] == "Positive"]
    posComments = positive_df["COMMENT"]

    print('Enter the Comment:')
    comment = input()
    tokens = preprocessingstage(comment)
    wordCount = len(tokens)
    bigramsOfComment = list(nltk.bigrams(tokens))

    negProbability = probabiliy(bigramsOfComment, negComments)
    posProbability = probabiliy(bigramsOfComment, posComments)

    print(Fore.YELLOW + "\nGiven comment is a,")
    # probabilities
    # print(Fore.YELLOW+"In given comment,\n"+ "Negative Probability = " + str(negProbability) +
         # "\nPositive Probability = " + str(posProbability))
    if posProbability > negProbability:
        print(Fore.BLUE+"Positive comment")
        pp = perplexity(posProbability, wordCount)
        print ("Perplexity = " + str(pp))
    else:
        if posProbability < negProbability:
            print(Fore.BLUE+"Negative comment")
            pp = perplexity(negProbability, wordCount)
            print(Fore.MAGENTA+"Perplexity = " + str(pp))
