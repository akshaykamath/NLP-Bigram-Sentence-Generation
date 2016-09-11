from __future__ import division
from collections import defaultdict
import random
from numpy.random import choice

wordCount = 0


def add_single_item_to_dict(dict, item):
    if item not in dict:
        dict[item] = 1
    else:
        dict[item] += 1


def readFile():
    with open('Dataset\\nonsense - Copy.txt') as f:
        lines = f.read().splitlines()
    return lines


def print_size_of_vocab():
    size = 0
    for word in vocabulary.keys():
        size += vocabulary[word]
        #print word

    print "vocab word count", size
    print "vocab size count", len(vocabulary.keys())


def print_size_of_extended_vocab():
    size = 0
    for word in extended_vocabulary.keys():
        size += extended_vocabulary[word]
        #print word

    print "extended vocab word count", size
    print "extended vocab size count", len(extended_vocabulary.keys())


def calculate_vocab():
    bigram_count = 0
    wordCount = 0
    lines = readFile()

    for line in lines:
        sentence = line.split()

        for i in range(0, len(sentence)):
            word = sentence[i]

            add_single_item_to_dict(vocabulary, word)

            wordCount += 1

            if word == "START123":
                continue

            else:
                previousWord = sentence[i - 1]
                bigram = (previousWord, word)
                add_single_item_to_dict(bigram_dict, bigram)
                bigram_count += 1


def calculate_extended_vocab():
    wordCount = 0
    for line in extended_vocabulary_arr:
        sentence = line.split()

        for i in range(0, len(sentence)):
            word = sentence[i]

            if word not in vocabulary:
                add_single_item_to_dict(extended_vocabulary, word)

            wordCount += 1

    #print wordCount


def bigram_probability():
    for bigram in bigram_dict.keys():
        try:
            probability = float(bigram_dict[bigram] / vocabulary[bigram[0]])
            bigram_probability_dict[bigram] = probability
            print bigram, ": ", probability
        except:
            bigram_probability_dict[bigram] = "NAN"
            print bigram, ": NAN"

    return bigram_probability_dict


def bigram_additive_smoothing_probability():
    print len(vocabulary.keys())
    size_of_vocabulary = len(vocabulary.keys())

    for bigram in bigram_dict.keys():
        try:
            probability = float( (bigram_dict[bigram] + 1)/ (vocabulary[bigram[0]] + size_of_vocabulary))
            bigram_prob_smoothing_dict[bigram] = probability
            print bigram, ": ", probability
        except:
            bigram_prob_smoothing_dict[bigram] = "NAN"
            print bigram, ": NAN"

    return bigram_prob_smoothing_dict


# Assumption here that the dcitionary being passed is the laplace smoothed vocab.
def get_sentence_probability(sentence, bigram_probability_dict):
    words = sentence.split()
    sentence_probability = 1

    # Subtract 4 for start and end markers in both the vocabs.
    vocab_size = len(vocabulary.keys()) + len(extended_vocabulary.keys())

    for i in range(0, len(words)):
        word = words[i]
        if word == "START123" :
            continue

        previousWord = words[i - 1]

        if (previousWord, word) in bigram_probability_dict:
            sentence_probability = sentence_probability * bigram_probability_dict[(previousWord, word)]
        else:
            denominator = 0
            # if previous word is in vocabulary, get the occurences of that word.
            # if not, just add the size of the vocab.

            if previousWord in vocabulary:
                denominator = vocabulary[previousWord]

            denominator += vocab_size
            bigram_probability = float(1 / denominator)
            sentence_probability = sentence_probability * bigram_probability

    print sentence, " ", sentence_probability
    return sentence_probability


# Generate Bigram Sentences.
def get_random_generated_bigram_sentences():
    selected_next_word = "START123"
    generated_words = []

    while 1:
        next_possible_word_tups = [(key[1], bigram_prob_dict[key]) for key in bigram_prob_dict.keys() if key[0] == selected_next_word]

        next_possible_words = [tuple[0] for tuple in next_possible_word_tups]
        conditional_probability_distribution = [tuple[1] for tuple in next_possible_word_tups]

        selected_next_word = choice(next_possible_words, 1, conditional_probability_distribution)

        if selected_next_word == "END123":
            break

        generated_words.append(selected_next_word[0])

    generated_sentence = ' '.join(generated_words)

    return generated_sentence

extended_vocabulary_arr = ["START123 I do not like them in a mouse . END123",
                           "START123 I am Sam I am Sam END123",
                           "START123 I do like them anywhere . END123",
                           "START123 I would like green ham and beef . END123"]


vocabulary = defaultdict(int)
bigram_dict = defaultdict(int)
bigram_probability_dict = defaultdict(int)
bigram_prob_smoothing_dict = defaultdict(int)
extended_vocabulary = defaultdict(int)

print "\n##################################################################\n"
calculate_vocab()
calculate_extended_vocab()
print_size_of_vocab()
print_size_of_extended_vocab()


print "\n##################################################################\n"
bigram_prob_dict = bigram_probability()

print "\n##################################################################\n"
bigram_prob_smoothing_dict = bigram_additive_smoothing_probability()

print "\n##################################################################\n"
get_sentence_probability("START123 I do not like them in a mouse . END123", bigram_prob_smoothing_dict)

print "\n##################################################################\n"
get_sentence_probability("START123 I am Sam I am Sam END123", bigram_prob_smoothing_dict)

print "\n##################################################################\n"
get_sentence_probability("START123 I do like them anywhere . END123", bigram_prob_smoothing_dict)


print "\n##################################################################\n"
get_sentence_probability("START123 I would like green ham and beef . END123", bigram_prob_smoothing_dict)


print "\n##################################################################\n"

generated_sentence = get_random_generated_bigram_sentences()

print generated_sentence
