import random


TOTAL_NUM_SENTENCES = 1000
NUM_CLUSTERS = 10
SENTENCES_PER_ARTICLE_PERCENTAGE = 20 / 100
NUM_SENTENCES_PER_CLUSTER = TOTAL_NUM_SENTENCES / NUM_CLUSTERS
NUM_SENTENCES_PER_ARTICLE = int(SENTENCES_PER_ARTICLE_PERCENTAGE * NUM_SENTENCES_PER_CLUSTER)
NUM_ARTICLES = int(NUM_SENTENCES_PER_CLUSTER / NUM_SENTENCES_PER_ARTICLE)
EXPANSION_RATE = NUM_CLUSTERS  # the number of articles to expand to from 1 article


# return a given number of random elements of arg_list
def get_random_elements_from_list(arg_list, num):
    random.shuffle(arg_list)
    random.shuffle(arg_list)
    if len(arg_list) < num:
        return arg_list
    return arg_list[:num]


# converts a text to a list of sentences
def extract_all_sentences(article_content):
    all_sentences = []
    for line in article_content:
        sentences = line.split(". ")
        sentences = list(filter(lambda sent: sent != "\n", sentences))
        map(lambda sent: all_sentences.append(sent+"\n"), sentences)
    return all_sentences


# get plain text and return a constant number of random sentences
def extract_sentences_from_article(article_content):
    sentences_list = extract_all_sentences(article_content)
    sentences = get_random_elements_from_list(sentences_list, NUM_SENTENCES_PER_ARTICLE)
    return sentences