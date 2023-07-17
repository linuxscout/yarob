import unittest

import sys
import pprint
sys.path.append("../web")
import re
import adaat
from  mysam.taginflector import tagInflector

class TestAdaatCase(unittest.TestCase):
    def setUp(self) :
        self.inflector = tagInflector()
        pass
    def test_lookup(self):
        """
        test create index
        """
        self.assertEqual(True, True)  # add assertion here
    def test_inflect(self):
        """
        test create index
        """
        phrase = "ليت الولد جميل"
        results = adaat.auto_inflect(phrase)
        pprint.pprint(results)
        self.assertEqual(True, True)  # add assertion here

    @unittest.skip("To do")
    def test_tag_inflect(self):
        """
        test create index
        """
        phrase = "ليت الولد جميل"
        phrase = "يلعب الولد ويجري بالكرتين"
        results = adaat.auto_inflect(phrase)
        pprint.pprint(results)
        for res in results:
            chosen = res.get("chosen","")
            inflct = res.get("inflect","")
            # Mishkal give an inflect string like this
            # '[---;------B;---]{}', 'STOPWORD:حرف::::حرف:إن و أخواتها:مبني:ناصب:T1G0N1'

            tagscode, inflect_string, taglist = self._extract_inflect(inflct)
            new_inflect_string = self.inflector.inflect(tagscode)
            print(chosen, inflct)
            print(tagscode, inflect_string, taglist)
            print(tagscode, new_inflect_string, taglist)
        self.assertEqual(True, False)  # add assertion here

    def test_tag_inflect_suggest(self):
        """
        test create index
        """
        phrase = "ليت الولد جميل"
        phrase = "يلعب الولد ويجري بالكرتين"
        word_features_table = adaat.auto_inflect(phrase, suggests=True)
        pprint.pprint(word_features_table)
        self.assertEqual(True, False)  # add assertion here

    def _extract_inflect(self, inflct):
        """
        A temporary function to split inflect string output from Mishkal into
        tagcode, inflect_string, taglist
        """
        # Mishkal give an inflect string like this
        # '[---;------B;---]{}', 'STOPWORD:حرف::::حرف:إن و أخواتها:مبني:ناصب:T1G0N1'
        fields = inflct.split("<br/>")
        tagcode= inflect_string = taglist = ""
        if len(fields)>=2:
            taglist = fields[1].split(":")
            x = re.search(r"(?<=\[)(.)+(?=\])", fields[0])
            if x:
                tagcode = x.group()
            x  = re.search(r"(?<=\{)(.)+(?=\})", fields[0])
            if x:
                inflect_string = x.group()
        return tagcode, inflect_string, taglist

    def test_highlite(self):
        """
        test high loghting similar on input phrase
        """
        sample_phrase = "أكل الوَلد تفاحة من يد أمه"
        input_phrase = "الولدُ يلعب أمه في"
        res_phrase  = adaat.highlite(sample_phrase, input_phrase)
        print(sample_phrase)
        print(input_phrase)
        print(res_phrase)
        self.assertEqual(True, False)  # add assertion here
if __name__ == '__main__':
    unittest.main()
