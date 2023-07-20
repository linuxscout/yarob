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
from  mysam.taginflector import tagInflector
from  mysam.tagcoder import tagCoder
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
        return auto_inflect(text, lastmark, suggests=True)
    elif action == "GetAll":
        # lastmark = options.get('lastmark', "0")
        return get_all(options)
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
        # res["inflection"] = res["inflection"].replace("\n","<br/>")
        # res["inflection"] = res["inflection"].replace(".",".<br/>")
        res["inflection"] = highlight_inflect(res["inflection"])
        res["phrase"] = highlite(res["phrase"], text)
        list_result.append(res)

    return list_result

def get_all(options={}):
    """
    Lookup for similar texts and give their inflections
    """
    # word_list = araby.tokenize(text)

    db =  samplesdb.SamplesDB()
    results = db.get_all()
    # results = db.lookup(text)

    list_result = []
    for res in list(results.values()):
        # a  dict contains keys : phrase, inflection, freq
        res["inflection"] = res["inflection"].replace("\n","<br/>")
        res["inflection"] = res["inflection"].replace(".",".<br/>")
        list_result.append(res)

    return list_result

def highlight_inflect(text):
    """
    High light inflection
    """
    hilited_lines = []
    lines = text.split(".")
    for line in lines:
        if ":" in line:
            parts = line.split(":")
            hilited_lines.append("<strong>%s</strong>: "%parts[0] + ":".join(parts[1:]))
        elif line.startswith("وجملة") or line.startswith("والجملة"):
            hilited_lines.append(line.replace("والجملة", "<strong>والجملة</strong>"))
        else:
            hilited_lines.append(line)
    return ".<br/>".join(hilited_lines)


def auto_inflect(text, lastmark="", suggests=False):
    """
    Generate Inflection for given text
    """
    inflector = tagInflector()
    tagcoder = tagCoder()
    cpath = os.path.join(os.path.dirname(__file__), '../tmp/')
    vocalizer = ArabicVocalizer.TashkeelClass(mycache_path = cpath)
    if lastmark == "0" or not lastmark:
        vocalizer.disable_last_mark()
    vocalized_listdict = vocalizer.tashkeel_ouput_html_suggest(text)
    if suggests:
        resultsListList, _ = vocalizer.full_stemmer(text)
        word_features_table = {}
        for resList in resultsListList:
            # print(type(resList))
            if resList:
                key = resList[0].get_unvocalized()
                word_features_table[key] = {}
            for rsdict in resList:
                vocalized = rsdict.get_vocalized();
                tags = rsdict.get_tags()
                typ = rsdict.get_type()
                tags = ":".join([tags, typ])
                # build tagcode string
                tagscode = tagcoder.encode(tags.split(":"))
                # build inflection string
                inflect = inflector.inflect(tagscode)
                # stoe date
                new_dict = {"vocalized": rsdict.get_vocalized(),
                            "type": typ,
                            "tags": tags,
                            "tagscode": tagscode,
                            "inflect":inflect,
                            }
                if vocalized in word_features_table[key]:
                    word_features_table[key][vocalized].append(new_dict)
                else :
                    word_features_table[key][vocalized] = [new_dict,]
        for voc_dict in vocalized_listdict:
            chosen_nm = araby.strip_tashkeel(voc_dict.get("chosen",''))
            voc_dict['features'] = word_features_table.get(chosen_nm, {})

    # return word_features_table
    return vocalized_listdict


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
