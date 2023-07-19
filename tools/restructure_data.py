#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# restructure_data.py
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
# --------
# Convert samples_data, into new struture
import sys
import pprint
import re
from pyarabic import araby

sys.path.append(".")
sys.path.append("../")
sys.path.append("../yarob")
sys.path.append("./tools")
sys.path.append("../tools")

import yarob.samples_const
# import yarob.samples_const2
from yarob import samplesdb
from tools import samples_temp


class Converter:
    def __init__(self, start=1):
        """
        init converter
        @start: id first value
        """
        self.id_counter = start
        self.samplesdb = yarob.samplesdb.SamplesDB()
        pass

    def _is_quran(self, text):
        """
        Test if the text contains Quran
        """
        patterns = ["قال تعالى",
            "قوله تعالى",
        ]
        for pat in patterns:
            if pat in text:
                return True
        return False

    def _is_hadith(self, text):
        """
        Test if the text contains Hadith
        """
        patterns = ["قال رسول الله",
            "صلى الله عليه وسلم",
            "عن النبي",
        ]
        for pat in patterns:
            if pat in text:
                return True
        return False

    def _is_poem(self, text):
        """
        Test if the text contains poem
        """
        patterns = ["قال الشاعر",
            "**",
        ]
        for pat in patterns:
            if pat in text:
                return True
        return False

    def _detect_type(self, text):
        """
        extract text type
        """
        if self._is_quran(text):
            return "قرآن"
        elif self._is_hadith(text):
            return "حديث"
        elif self._is_poem(text):
            return "شعر"
        return ""

    def _get_id(self):
        """
        add an ID
        """
        id = self.id_counter
        self.id_counter+=1
        return id

    def _get_unvocalized(self, text):
        """
        strip tashkeel
        """
        return araby.strip_tashkeel(text)
    def _clean(self, text):
        """
        strip mark unicode and spaces
        """
        text = text.replace("\u202a", "")
        text = text.replace("\u202b", "")
        text = text.replace("\u202c", "")
        text = text.strip()
        text = re.sub(r'\s+', ' ', text)
        return text
    def _structure_inflection(self, text):
        """
        advance structured inflections
        return a list of dict, each dict represent a word inflect, or a sub phrase inlfection
        the dict must contains:
        - token: represent the word/part of wordn sub phrase
        -  type : word/part of word/sub-phrase
        - detailled infection of given token
        }
        @return: a list of dict
        """
        return []

    def _get_state(self, value):
        """
        strip tashkeel
        """
        if value:
            return "draft"
        else:
            return "todo"


    def _get_lemmas(self, text: str) -> list:
        """
        extract a list of lemmas from given text
        """
        return ":".join(self.samplesdb._get_phrase_lemmas(text))

    def convert(self, samples=None):
        """
        convert samples data into new struture
        @return: new data structure
        """
        # We will restructure samples
        # use id as key instead of unvoalied phrase
        # extract type if possible, and add "to review" to chek it
        # Add source field as empty, to be filled manually
        # Add vocalized phrase field
        # Add unvocalized phrase field
        # Add unvocalized phrase field
        # add keywords or terms to be used in index
        # replace checked by state
        # To do: retructure Inflection data
        if not samples:
            samples = yarob.samples_const.SAMPLES
        new_samples = {}
        for key in samples:
            # the new key is an ID
            new_key =  self._get_id()
            item = samples[key]
            # deep copy of item
            new_item = {}
            new_item["id"] = new_key
            new_item["phrase"] = self._clean(item.get("phrase",""))
            new_item["inflection"] = self._clean(item.get("inflection",""))
            new_item["structured_inflection"] = item.get("structured_inflection",
                                                         self._structure_inflection(new_item["inflection"]))
            # if unvocalized not exists, strip tashkeel from phrase
            new_item["unvocalized"] = self._get_unvocalized(item.get("phrase",""))
            new_item["source"] = item.get("source","")
            new_item["reference"] =  item.get("reference","")
            new_item["date"] =  item.get("date","")
            # if state non exist, try checked
            new_item["state"] =   item.get("state", self._get_state(item.get("checked","")))
            new_item["type"] =  item.get("type","")

            # extract new type:
            phrase_type = item.get("type","")
            if not phrase_type:
                phrase_type = self._detect_type(new_item.get("unvocalized",""))
                if phrase_type:
                    new_item["state"] = "to review"
                    new_item["type"] = phrase_type

            # add keywords or terms to be used in index
            new_item["keywords"] = self._get_lemmas(new_item["unvocalized"])
            #
            new_samples[new_key] = new_item
        return new_samples


def main(args):

    conv = Converter(start=1)
    new_samples = conv.convert()
    # new_samples = conv.convert(samples_temp.SAMPLES)
    # new_samples = conv.convert(yarob.samples_const2.SAMPLES)
    pprint.pprint(new_samples)

    print("*************")
    cpt = 0
    show_type_detect = False
    show_type_detect = True
    to_review = {}
    if show_type_detect:
        for key in new_samples:
            if new_samples[key]['state'] == "to review":
                cpt +=1
                to_review[key] = new_samples[key]
        pprint.pprint(to_review)                
        print("# number of to review ",cpt)
    # pprint.pprint({key: new_samples[key] for key  in new_samples if new_samples[key]['state'] == "to review"})

    return 0


if __name__ == '__main__':
    import sys

    sys.exit(main(sys.argv))
