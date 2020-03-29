import urllib.request
import random
import requests
import queue
import wikipedia
from bs4 import BeautifulSoup


def remove_duplicates(sorted_list):
    sorted_list = map(lambda url: url.split('#')[0], sorted_list)
    uniques = list(dict.fromkeys(sorted_list))
    return uniques


def simple_wiki_ref(url):
    return url is not None and len(url.split(':')) == 1 and url.startswith("/wiki")


def get_page_soup(page_address):
    page = requests.get(page_address).text
    soup = BeautifulSoup(page, "html.parser")
    return soup


def get_all_refs_from_page(page_address):
    soup = get_page_soup(page_address)
    inside_refs = soup.find_all('a')
    results = map(lambda link: link.get('href'), inside_refs)
    return results


def get_wiki_refs_from_page(page_address):
    results = get_all_refs_from_page(page_address)
    filter_result = filter(lambda url: url is not None and not url.startswith("#"), results)
    filter_result = list(filter_result)
    filter_result.sort()
    filter_result = remove_duplicates(filter_result)
    types = filter(simple_wiki_ref, filter_result)
    full_urls = list(map(lambda url: WIKI_MAIN_URL + url, types))
    return full_urls


def extract_all_sentences(url):
    content_list = get_page_soup(url).find_all('p')
    content_list = list(map(lambda p: p.get_text(), content_list))
    all_sentences = []
    for line in content_list:
        sentences = line.split(". ")
        for sent in sentences:
            all_sentences.append(sent+"\n")
    return all_sentences


def get_random_elements_from_list(arg_list, arg_num_elements):
    random.shuffle(arg_list)
    random.shuffle(arg_list)
    if len(arg_list) < arg_num_elements:
        return arg_list
    return arg_list[:arg_num_elements]


def extract_sentences_from_article(article, num_sentences):
    sentences_list = extract_all_sentences(article)
    sentences = get_random_elements_from_list(sentences_list, num_sentences)
    return sentences


def get_more_articles(start_article, num_articles):
    wiki_refs = get_wiki_refs_from_page(start_article)
    ref_articles = get_random_elements_from_list(wiki_refs, num_articles)
    return ref_articles


def write_list_to_file(sentences_list, url, filehandler):
    article_name = url.split('/')[-1]
    for sentence in sentences_list:
        if sentence == "\n":
            continue
        try:
            filehandler.write(article_name + '\t %s' % sentence)
        except UnicodeEncodeError:
            print("error in writing sentence: " + article_name + '\t %s' % sentence)


FULL_FILE_NAME = 'random_wikipedia_sentences'
WIKI_MAIN_URL = "https://en.wikipedia.org"
TOTAL_NUM_SENTENCES = 1000
NUM_CLUSTERS = 10
SENTENCES_PER_ARTICLE_PERCENTAGE = 20 / 100
num_sentences_per_cluster = TOTAL_NUM_SENTENCES / NUM_CLUSTERS
num_sentences_per_article = int(SENTENCES_PER_ARTICLE_PERCENTAGE * num_sentences_per_cluster)
NUM_ARTICLES = num_sentences_per_cluster / num_sentences_per_article
EXPANSION_RATE = NUM_CLUSTERS  # the number of articles to expand to from 1 article


def get_all_sentences(url, file_name):
    count = 0
    articles_queue = queue.Queue()
    articles_queue.put(url)
    with open(file_name, encoding='utf-8', mode='w+') as filehandler:
        while count < num_sentences_per_cluster:
            curr_url = articles_queue.get()
            print(curr_url)
            children = get_more_articles(curr_url, EXPANSION_RATE)
            for child in children:
                articles_queue.put(child)
            batch = extract_sentences_from_article(curr_url, num_sentences_per_article)
            write_list_to_file(batch, curr_url, filehandler)
            count += len(batch)
            print(count)


seeds = wikipedia.random(NUM_CLUSTERS)
for i in range(len(seeds)):
    full_url = WIKI_MAIN_URL+"/"+seeds[i]
    write_to_file = FULL_FILE_NAME+"_" + str(i) + ".txt"
    get_all_sentences(full_url, write_to_file)

