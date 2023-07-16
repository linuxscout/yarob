#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  adaat.py
#  
#  Copyright 2020 zerrouki <zerrouki@majd4>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
#system lib
import os.path
import sys
import random

# external
import mishkal.tashkeel as ArabicVocalizer
import pyarabic.araby as araby

# local
import randtext
sys.path.append(os.path.join("../yarob"))

import samplesdb

# ~ import phrase_generator
def DoAction(text, action, options = {}):
    """
    do action by name
    """
    if action == "DoNothing":
        return text
    elif action == "phrase":
        return build_phrase(options)
    elif action == "sample":
        return build_sample(options)
    elif action == "RandomText":
        return random_text() 
    elif action == "Tashkeel2":
        lastmark = options.get('lastmark', "0")    
        return tashkeel2(text, lastmark)               
    elif action == "Lookup":
        lastmark = options.get('lastmark', "0")    
        return lookup_inflect(text, lastmark)               
    elif action == "Inflect":
        lastmark = options.get('lastmark', "0")    
        return auto_inflect(text, lastmark)               
    else:

        return text

def build_phrase(options):        
    phraser = phrase_generator.PhraseGenerator()
    components = options
    phrase = phraser.build(components)
    #~ print(u"".join(["<%s>"%x for x in components.values()]))
    #~ print(phraser.pattern.stream.__str__())
    return phrase

def build_sample(options):        
    """generate samples"""
    return repr(options).replace(",", ",\n")
    
def random_text():
    """
    get random text for tests
    """    
    return random.choice(randtext.textlist)

def tashkeel2(text, lastmark):
    """
    Tashkeel text with suggestions
    """
    cpath = os.path.join(os.path.dirname(__file__), '../tmp/')
    vocalizer = ArabicVocalizer.TashkeelClass(mycache_path = cpath)
    #~ vocalizer.disable_cache()
    if lastmark == "0" or not lastmark:
        vocalizer.disable_last_mark()    
    vocalized_dict = vocalizer.tashkeel_ouput_html_suggest(text)
    return vocalized_dict    
    
# ~ def lookup_inflect(text, lastmark):
    # ~ """
    # ~ Lookup for similar phrase in data base,
    # ~ ordred by revelence
    # ~ """
    # ~ cpath = os.path.join(os.path.dirname(__file__), '../tmp/')
    # ~ vocalizer = ArabicVocalizer.TashkeelClass(mycache_path = cpath)
    # ~ #~ vocalizer.disable_cache()
    # ~ if lastmark == "0" or not lastmark:
        # ~ vocalizer.disable_last_mark()    
    # ~ vocalized_dict = vocalizer.tashkeel_ouput_html_suggest(text)
    # ~ return vocalized_dict 

# def lookup_inflect(text, last_mark=""):
#     """
#     Lookup for similar texts and give their inflections
#     """
#     word_list = araby.tokenize(text)
#
#     if not word_list:
#         return []
#     else:
#         list_result = []
#         for word in word_list:
#             word_nm = araby.strip_tashkeel(word)
#             tag = 'إعراب الكلمة'
#             list_result.append({'word':word, 'tag': tag})
#         return list_result

def lookup_inflect(text, last_mark=""):
    """
    Lookup for similar texts and give their inflections
    """
    # word_list = araby.tokenize(text)
    
    db =  samplesdb.SamplesDB()
    results = db.match(text)
    # results = db.lookup(text)

    list_result = []
    for res in results:
        # a  dict contains keys : phrase, inflection, freq
        res["inflection"] = res["inflection"].replace("\n","<br/>")
        res["phrase"] = highlite(res["phrase"], text)
        list_result.append(res)

    return list_result

def auto_inflect(text, lastmark=""):
    """
    Generate Inflection for given text
    """
    cpath = os.path.join(os.path.dirname(__file__), '../tmp/')
    vocalizer = ArabicVocalizer.TashkeelClass(mycache_path = cpath)
    #~ vocalizer.disable_cache()
    if lastmark == "0" or not lastmark:
        vocalizer.disable_last_mark()    
    vocalized_dict = vocalizer.tashkeel_ouput_html_suggest(text)
    return vocalized_dict


def highlite(output_ph, input_ph):
    """
    Highlight words in output which are similar to words in input
    """
    # compare out tokens to in tokens without diacritics
    in_tokens = araby.tokenize(input_ph, morphs=[araby.strip_tashkeel])
    # keep diacritics to display string properly
    out_tokens = araby.tokenize(output_ph)
    res_tokens = []
    for outtok in out_tokens:
        outtok_nm = araby.strip_tashkeel(outtok)
        if outtok_nm in in_tokens:
            res_tokens.append('<span class="diff-mark">%s</span>'%outtok)
        else:
            res_tokens.append(outtok)
    return " ".join(res_tokens)

def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
