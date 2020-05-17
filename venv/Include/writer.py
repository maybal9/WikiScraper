FULL_FILE_NAME = 'random_wikipedia_sentences'


def write_all_textlines_to_file(textlines, filename):
    outfile = open(filename, encoding='utf-8', mode='w+')
    outfile.writelines(textlines)
    outfile.close()


def create_filename(i):
    return FULL_FILE_NAME+"_" + str(i) + ".txt"
