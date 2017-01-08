#!/usr/bin/python3
#!encoding=UTF-8

import math
import numpy as np
#import lda

"""
    tools for counting the statistics of things.
    @authors matthew g mcgovern, 

"""

def count_symbol_frequency( text ):
    """ Count the frequency of symbol occurances in a body of text.
    """
    frequencies = dict()
    for ch in text:
        if ch in frequencies:
            frequencies[ch] += 1
        else:
            frequencies[ch] = 1
    return frequencies

def count_n_gram_frequency( raw_list ):
    """ count the frequency that phrases and words appear in a text,
     when passed the list of phrases (which are kept as lists). 
     It's a list of lists.
    """
    frequencies = dict()
    for sub_list in raw_list: #for each sub list in the list
        items = [item for item in sub_list ]
        joined = " ".join( items ) #flatten it into a string
        #and count that ish
        if joined in frequencies:
            frequencies[joined] += 1
        else:
            frequencies[joined] = 1 
    return frequencies

def calculate_symbol_entropy( frequency_dict ):
    """ 
        returns the entropy of a symbol frequency list.
        thiiis might not be correct
    """
    distinct_symbol_count = len( frequency_dict )
    return -sum( frequency/distinct_symbol_count * math.log(frequency/distinct_symbol_count, 2) for frequency in frequency_dict.values() ) 

def generate_list_of_raw_ngrams( split_text, up_to_length ):
    """
    Gathers frequency data for n-grams (words and phrases up to length n).
    Pass a body of text and the length N that you want the phrases to be.
    """
    list_of_ngrams = []
    for j in range(1, up_to_length+1): #inclusive
        for i in range(0, len(split_text)):
            n_gram = split_text[i:i+j]
            if len( n_gram) == j:
                list_of_ngrams.append( n_gram  )
    return list_of_ngrams

def count_n_grams( text, up_to_length, logographic=False ):
    split_text = None
    """
    if logographic:
        split_text = [ ch for ch in text ]
        #print( split_text )
    """ 
    
    split_text = split_with_selector(text, include_dubious=False)
        #print( split_text )
    raw_ngrams = generate_list_of_raw_ngrams( split_text , up_to_length )
    #print(  raw_ngrams )
    n_gram_count = count_n_gram_frequency( raw_ngrams )
    return n_gram_count


def set_up_character_ranges_table():
    # (low, high, string_name )
    ranges = []
    with open( 'unicode_ranges.txt', 'r') as range_file:
        for line in range_file:
            split = line.split()
            joined = [ int( split[0], 16 ), int(split[1], 16), " ".join(split[2:]) ]
            #print( joined )
            ranges.append( joined )
    return ranges

def check_ranges_from_table( character, table ):
    order = ord(character) 
    for i in range( 0 ,len(table)):
        if table[i][0] <= order and order <= table[i][1]:
            #print( character, " is from character set ", table[i][2])
            return table[i][2]

#shoutout to the lda demo code.

"""
def run_lda( matrix ):
    lda_model = lda.LDA(n_topics=50, n_iter=2000, random_state=1)
    lda_model.fit(matrix)
    return lda_model

def print_lda_topic_results( post_run_model, vocabulary, document_titles):
    n_top_words = 9
    for i, topic_distribution in enumerate(model.topic_word_):
        topic_words = np.array(vocabulary)[np.argsort(topic_distribution)][:-n_top_words:-1]
        print('Topics {}: {}'.format(i,' '.join(topic_words)))

def print_lda_document_topic_results( model, vocab, document_titles, how_many ):
    document_topic = model.doc_topic_
    for i in range( how_many ):
        print("{} (top topic: {})".format(titles[i], document_topic[i].argmax()))
""" 

from voynich import *

if __name__ == "__main__":
    import sys
    assert( len(sys.argv )> 1  )
    in_file = sys.argv[1] 
    with open( in_file, 'r', encoding="latin-1") as inputfile:
        body = ""
        for line in inputfile:
            if line[0] != '#' and parse_line_header(line, transcription='F', page=39):
                line = remove_comments(line)
                line = remove_filler(line)
                line = remove_breaks(line)
                body += remove_line_header(line)
        print( body )
        symb_freq = count_symbol_frequency(body)
        entropy = calculate_symbol_entropy(symb_freq)
        ng = count_n_grams( body, 5, logographic=False )
        print( 'symbols:', symb_freq )
        print( ng )

        print( 'entropy:', entropy )
    

    """
    test_text = "Do you love me or do you love me not?" #ima be me
    test_text2 =  "你爱不爱我？"

    print("SYMBOL FREQUENCY:")
    test1 = count_symbol_frequency(test_text)
    print( test1, calculate_symbol_entropy(test1) )

    test2 = count_symbol_frequency(test_text2)
    print( test2, calculate_symbol_entropy(test2 ) )

    print("NGRAM FREQUENCY:")
    print( count_n_grams( test_text2, 5, logographic=True ) )
    print( count_n_grams( test_text, 5, logographic=False ) )

    table = set_up_character_ranges_table()
    print("LANGUAGE IDENT FROM UNICODE:")
    print( check_ranges_from_table( '你' , table) )
    print( check_ranges_from_table( 'L' , table) )
    print( check_ranges_from_table( 'ᜊ' , table) )
    print( check_ranges_from_table( 'ʃ' , table) )
    print( check_ranges_from_table( 'к' , table) )
    ##import lda.datasets
    
    # demo = lda.datasets.load_reuters()
    # vocab = lda.datasets.load_reuters_vocab()
    # titles = lda.datasets.load_reuters_titles()

    # model = run_lda( demo )
    # print_lda_document_topic_results(model, vocab, titles, 10)
    # print_lda_topic_results(model, vocab, titles) 
    
    #print( "woot")
    """
