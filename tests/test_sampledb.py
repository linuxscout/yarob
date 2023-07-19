import unittest

import sys
import pprint

from pyarabic import araby

sys.path.append("../")
sys.path.append("./")

from yarob.samplesdb import SamplesDB
import yarob.samples_const
import samples_temp


class TestSampleDBCase(unittest.TestCase):
    def setUp(self) :
        self.db = SamplesDB()
        pass

    def test_create_index(self):
        """
        test create index
        """
        word_index = self.db.create_index()
        pprint.pprint(word_index)
        # check non arabic words in index
        non_arabic_words = [w for w in word_index if not araby.is_arabicword(w)]
        print("index size ",len(word_index))
        print("index size ",len(word_index.keys()))
        self.assertEqual(len(word_index.get("",[])), 0, " Index contains Empty words")  # add assertion here
        self.assertEqual(len(non_arabic_words), 0, " Index contains non Arabic word")  # add assertion here
        self.assertEqual(len(word_index), 3176, " Index size changed")  # add assertion here

    def test_temp_create_index(self):
        """
        test create index
        """
        word_index = self.db.create_index(samples_temp.SAMPLES)
        pprint.pprint(word_index)
        # check non arabic words in index
        non_arabic_words = [w for w in word_index if not araby.is_arabicword(w)]
        print("index size ",len(word_index))
        print("index size ",len(word_index.keys()))
        self.assertEqual(len(word_index.get("",[])), 0, " Index contains Empty words")  # add assertion here
        self.assertEqual(len(non_arabic_words), 0, " Index contains non Arabic word")  # add assertion here
        self.assertEqual(len(word_index), 2147, " Index size changed")  # add assertion here


    def test_build_index(self):
        """
        test create index within the class
        """
        word_index = self.db._build_index()
        pprint.pprint(word_index)
        # check non arabic words in index
        non_arabic_words = [w for w in word_index if not araby.is_arabicword(w)]
        print("index size ",len(word_index))
        print("index size ",len(word_index.keys()))
        self.assertEqual(len(word_index.get("",[])), 0, " Index contains Empty words")  # add assertion here
        self.assertEqual(len(non_arabic_words), 0, " Index contains non Arabic word")  # add assertion here
        self.assertEqual(len(word_index), 3176, " Index size changed")  # add assertion here

    # @unittest.skip("to do")
    def test_match_index(self):
        """
        test create index
        """
        phrase = "ليت الولد جميل"
        inflect_dict = self.db.match(phrase)
        pprint.pprint(inflect_dict)
        print(len(inflect_dict))
        self.assertEqual(len(inflect_dict), 30)  # add assertion here

    # @unittest.skip("to do")
    def test_check_duplicata(self):
        """
        test create index
        """
        sm = yarob.samples_const.SAMPLES
        dups = []
        cpt = 0
        for id1 in sm:
            for id2 in sm:
                if id1 != id2 and id1< id2:
                    if sm[id1]["unvocalized"] == sm[id2]["unvocalized"]:
                        if sm[id1]["state"] != "remove" and sm[id2]["state"] != "remove":
                            dups.append((id1, id2, sm[id1]["unvocalized"]))
        print("--- Duplicated cases ---")
        pprint.pprint(dups)
        self.assertEqual(len(dups), 0, "There are duplicata")  # add assertion here


if __name__ == '__main__':
    unittest.main()
