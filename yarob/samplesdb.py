#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  samplesdb.py
#  
#  Copyright 2023 zerrouki <zerrouki@majd4>
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
import copy
from difflib import SequenceMatcher
import pickle
from pyarabic import araby
import qalsadi.analex
import qalsadi.stemnode

# try:
#     from . import samples_temp
# except ImportError:
#     import samples_temp
try:
    from . import samples_const
except:
    import samples_const


class SamplesDB:
    """
    A class to handle Inflection Samples and Data bases
    """
    def __init__(self, path=""):
        
        self.data  = samples_const.SAMPLES
        # self.data = samples_temp.SAMPLES
        self.analyzer = qalsadi.analex.Analex()
        self.index = self._build_index()
        self.path = path

    def _get_lemmas(self, word):
        """
        get all lemmas of a word
        """
        resultslist = self.analyzer.check_word(word)
        stmnd = qalsadi.stemnode.StemNode(resultslist)
        lemmas = stmnd.get_lemmas()
        lemmas = [araby.strip_tashkeel(lm) for lm in lemmas]
        return lemmas

    def _get_phrase_lemmas(self, phrase_nm):
        """
        get all lemmas of a phrase
        """

        tokens = araby.tokenize(phrase_nm)
        lemmas_list = []
        for tok in tokens:
            lemmas_list.extend(self._get_lemmas(tok))
        lemmas_list = list(set(lemmas_list))
        return lemmas_list

    def _build_index(self,):
        """

        """
        filename = "yarob_samplesdb_index.pickle"
        try:
            word_index = pickle.load(open(filename, "rb"))
        except (OSError, IOError):
            word_index = self.create_index(self.data)
            pickle.dump(word_index, open(filename, "wb"))

        return word_index

    def create_index(self, data={}):
        """
        Create index of words in samples,
        Can create an index for a given data
        can enbale or disable cache
        """
        if not data:
            data = self.data
        word_index = {}
        for id_key in data:
            # lemmas are already calculted in data dict
            lemmas = data[id_key].get("keywords","")
            if lemmas:
                lemmas = lemmas.split(":")
            else:
                phrase = data[id_key].get("phrase", "")
                lemmas = self._get_phrase_lemmas(phrase)
            for lem in lemmas:
                if araby.is_arabicword(lem):
                    if lem in word_index:
                        word_index[lem].append(id_key)
                    else:
                        word_index[lem] = [id_key]
        return word_index

    def lookup(self, phrase=""):
        """
        Look up for phrase in samples data, exact search.
        """
        return self._fake_lookup(phrase=phrase)
    
    def match(self, phrase=""):
        """
        Look up for phrase in samples data, approximative search.
        return a list of inflections dict with similarity score.
        """
        # tokenize phrase
        phrase_nm = araby.strip_tashkeel(phrase)
        # get all lemmas
        tokens = self._get_phrase_lemmas(phrase_nm)
        candidates_phrases = []
        # look up for all phrases containing tokens
        candidates_doc = self._get_ids_from_index(tokens)
        candidates_doc = list(set(candidates_doc))
        # order candidate_phrases according to their frequency
        # more a phrase contains tokens it will be selected
        # ~ phrase_frequency = dict(collections.Counter(candidates_phrases))
        candidates_inflections = []
        for cand_id in candidates_doc:
            # add frequency for each phrase
            data_inflect = copy.deepcopy(self.data.get(cand_id, {}))
            cand_phrase = data_inflect.get("unvocalized","")
            data_inflect["freq"] = self._similar(cand_phrase, phrase_nm)
        # data_inflect["freq"] = round(phrase_frequency.get(cand_phrase, 0)*100//len(tokens))
            data_inflect["checked"] = True
            candidates_inflections.append(data_inflect)
        # order candidate results according to frequency
        newlist = sorted(candidates_inflections, key=lambda d: d['freq'], reverse=True)
        # use deep copy temporary to avoid problems with data structure
        result_list = copy.deepcopy(newlist)
        return result_list
        # return self._fake_match(phrase)

    def get_all(self,options={}):
        """
        return Data
        """
        return copy.deepcopy(samples_const.SAMPLES)

    def _get_ids_from_index(self, tokens):
        """
        return all ids from word indexes
        """
        ids = []
        for tok in tokens:
            ids.extend(self.index.get(tok, []))
        return ids
    @staticmethod
    def _similar(a, b):
        """
        return similarity between candidate phrase and given phrase
        """
        sim = SequenceMatcher(None, a, b).ratio()
        return round(sim*100)

    @staticmethod
    def _fake_lookup(phrase):
        """
        Look up for phrase in samples data, exact search.
        Used just for testing
        """ 
        return [{"phrase": phrase,
                "inflection": "إعراب الجملة", },
                {"phrase": phrase,
                 "inflection": "2إعراب الجملة",
                 },
                ]

    @staticmethod
    def _fake_match(phrase):
        """
        Look up for phrase in samples data, approximative search.
        return a list of inflections dict with similarity score.
        """
        return [{"phrase": phrase+"1",
                 "inflection": "إعراب الجملة", },
                {"phrase": phrase+"2",
                 "inflection": "إعراب الجملة", }, ]

    def get_by_id(self,rec_id, options={}):
        """
        return Data by id
        """
        return  self.data.get(rec_id, {})


def main():
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
