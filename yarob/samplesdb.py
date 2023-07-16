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
import collections
import copy
from pyarabic import araby
try:
    from . import samples_const
except:
    import samples_const

class SamplesDB():
    """
    A class to handle Inflection Samples and Data bases
    """
    def __init__(self, path=""):
        
        self.data  = samples_const.SAMPLES
        self.index = self.create_index()
        
    def create_index(self,):
        """
        Create index of words in samples
        """
        word_index = {}
        for phrase_key in self.data:
            # tokenize phrase into words:
            tokens = araby.tokenize(phrase_key)
            for tok in tokens:
                if araby.is_arabicword(tok):
                    if tok in word_index:
                        word_index[tok].append(phrase_key)
                    else:
                        word_index[tok] = [phrase_key]
        return word_index
    
    
    def lookup(self, phrase =""):
        """
        Look up for phrase in samples data, exact search.
        """
        return self._fake_lookup(phrase)
    
    def match(self, phrase =""):
        """
        Look up for phrase in samples data, approximative search.
        return a list of inflections dict with similarity score.
        """
        # tokenize phrase
        phrase_nm = araby.strip_tashkeel(phrase)
        tokens = araby.tokenize(phrase_nm)
        # remove duplicated tokesn
        tokens = list(set(tokens))
        candidates_phrases = []
        # look up for all phrases containing tokens
        for tok in tokens:
            candidates_phrases.extend(self.index.get(tok,[]))
        # order candidate_phrases according to their frequency
        # more a phrase contains tokens it will be selected
        phrase_frequency = dict(collections.Counter(candidates_phrases))
        candidates_inflections = []
        for cand_phrase in phrase_frequency:
            # add frequency for each phrase
            data_inflect = self.data.get(cand_phrase, {})
            data_inflect["freq"] = round(phrase_frequency.get(cand_phrase, 0)*100//len(tokens))
            data_inflect["checked"] = True
            candidates_inflections.append(data_inflect)
        # order candidate results according to frequency
        newlist = sorted(candidates_inflections, key=lambda d: d['freq'], reverse=True)
        # use deep copy temporary to avoid problems with data structure
        result_list = copy.deepcopy(newlist)
        return result_list
        # return self._fake_match(phrase)

    def _fake_lookup(self, phrase):
        """
        Look up for phrase in samples data, exact search.
        Used just for testing
        """ 
        return [{"phrase":phrase,
            "inflection": "إعراب الجملة",
        },
                {"phrase": phrase,
                 "inflection": "2إعراب الجملة",
                 },
                ]
        
    def _fake_match(self, phrase):
        """
        Look up for phrase in samples data, approximative search.
        return a list of inflections dict with similarity score.
        """
        return [{"phrase":phrase+"1",
            "inflection": "إعراب الجملة",
        }    ,
        {"phrase":phrase+"2",
            "inflection": "إعراب الجملة",
        }   ,       
        ]
        
def main(args):
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
