import unittest

import sys
import pprint
sys.path.append("../")

from yarob.samplesdb import SamplesDB


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
        print(len(word_index))
        self.assertEqual(True, True)  # add assertion here
    def test_match_index(self):
        """
        test create index
        """
        phrase = "ليت الولد جميل"
        inflect_dict = self.db.match(phrase)
        pprint.pprint(inflect_dict)
        self.assertEqual(True, False)  # add assertion here


if __name__ == '__main__':
    unittest.main()
