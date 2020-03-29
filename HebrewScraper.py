import wikipedia
import queue
import random

wikipedia.set_lang("he")
page_title = wikipedia.random()
he_wiki_page = wikipedia.page(title=page_title)
print(he_wiki_page.summary)


num_sentences_per_cluster = 100
EXPANSION_RATE = 10
num_sentences_per_article = 50


def get_random_elements_from_list(arg_list, arg_num_elements):
    random.shuffle(arg_list)
    random.shuffle(arg_list)
    if len(arg_list) < arg_num_elements:
        return arg_list
    return arg_list[:arg_num_elements]


def extract_sentences_from_article(article, num_sentences):
    print("INFO: loading {}".format(article))
    page = wikipedia.page(title=article)
    content = page.content
    all_sentences = content.split(". ")
    sentences = get_random_elements_from_list(all_sentences, num_sentences)
    return sentences


def get_wiki_refs_from_page(page_address):
    results = wikipedia.page(page_address).links
    filter_result = filter(lambda url: url is not None and not url.startswith("#"), results)
    filter_result = list(filter_result)
    filter_result.sort()
    full_urls = list(map(lambda url: WIKI_MAIN_URL + url, types))
    return full_urls


def get_more_articles(start_article, num_articles):
    wiki_refs = get_wiki_refs_from_page(start_article)
    ref_articles = get_random_elements_from_list(wiki_refs, num_articles)
    return ref_articles


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