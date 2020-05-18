import queue
import wikipedia
import text_utilities
import writer


TOTAL_NUM_SENTENCES = 100
NUM_CLUSTERS = 10
SENTENCES_PER_ARTICLE_PERCENTAGE = 20 / 100
NUM_SENTENCES_PER_CLUSTER = TOTAL_NUM_SENTENCES / NUM_CLUSTERS
NUM_SENTENCES_PER_ARTICLE = int(SENTENCES_PER_ARTICLE_PERCENTAGE * NUM_SENTENCES_PER_CLUSTER)
NUM_ARTICLES = int(NUM_SENTENCES_PER_CLUSTER / NUM_SENTENCES_PER_ARTICLE)
EXPANSION_RATE = NUM_CLUSTERS  # the number of articles to expand to from 1 article


def get_wiki_page(article_name):
    try:
        wiki_page = wikipedia.page(title=article_name)
        return wiki_page
    except wikipedia.exceptions.DisambiguationError as err:
        # always take the first option
        wiki_title = err.options[0]
        print(wiki_title)
        wiki_page = wikipedia.page(wiki_title)
        return wiki_page
    except wikipedia.exceptions.PageError:
        wiki_page = get_wiki_page(wikipedia.random())
        return wiki_page


# given a wiki start url returns a list of more article names references
def get_more_articles(article_name):
    wiki_page = get_wiki_page(article_name)
    wiki_page_refs = wiki_page.links
    ref_articles = text_utilities.get_random_elements_from_list(wiki_page_refs, EXPANSION_RATE)
    return ref_articles


# given a article title return some random sentences
def process_one_article(article_name):
    wiki_page = get_wiki_page(article_name)
    article_content = wiki_page.content
    mini_batch = text_utilities.extract_sentences_from_article(article_content)
    return mini_batch


# main function!
# given a wiki valid start article name, return a batch of sentences
def produce_sentences_batch(first_article_title):
    batch = []
    count = 0
    articles_queue = queue.Queue()
    articles_queue.put(first_article_title)
    while count < NUM_SENTENCES_PER_CLUSTER:
        curr_article_title = articles_queue.get()
        children = get_more_articles(curr_article_title)
        list(map(articles_queue.put, children))
        mini_batch = process_one_article(curr_article_title)
        batch.extend(mini_batch)
        count += len(mini_batch)
    return batch


# given a language (language code) scrape sentences from wikipedia
def scrape_wiki(lang):
    # TODO: handle exceptions!
    wikipedia.set_lang(lang)
    # TODO: support NUM_CLUSTERS > 10
    seeds = wikipedia.random(NUM_CLUSTERS)
    for i in range(len(seeds)):
        # TODO: add debug mode
        print("STATUS: starting with {}".format(seeds[i]))
        text_lines = produce_sentences_batch(seeds[i])
        filename = writer.create_filename(i)
        writer.write_all_textlines_to_file(text_lines, filename)
        print("STATUS: finished creating {}".format(filename))


# scrape_wiki("he")
