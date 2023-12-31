import unittest

import sys
import pprint

from pyarabic import araby

sys.path.append("../")
sys.path.append("./")

from yarob.samplesdb_sql import SamplesDB_SQL
import yarob.samples_const
import samples_temp


class TestSampleDB_SQL_Case(unittest.TestCase):
    def setUp(self) :
        self.db = SamplesDB_SQL()
        # self.db.load_fake_data()
        # self.db.load_samples_data()
        # self.db._build_index()
        pass
    # @unittest.skip("to do")
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
        self.assertEqual(len(word_index), 3142, " Index size changed")  # add assertion here


    def test_temp_create_index(self):
        """
        test create index
        """
        # for all data
        # data = samples_temp.SAMPLES
        # data base
        data = self.db.get_all()

        word_index = self.db.create_index(data)
        pprint.pprint(word_index)
        # check non arabic words in index
        non_arabic_words = [w for w in word_index if not araby.is_arabicword(w)]
        print("index size ",len(word_index))
        print("index size ",len(word_index.keys()))
        self.assertEqual(len(word_index.get("",[])), 0, " Index contains Empty words")  # add assertion here
        self.assertEqual(len(non_arabic_words), 0, " Index contains non Arabic word")  # add assertion here
        self.assertEqual(len(word_index), 3142, " Index size changed")  # add assertion here

    @unittest.skip("done")
    def test_build_index(self):
        """
        test create index within the class
        """
        word_index = self.db._build_index()
        # pprint.pprint(word_index)
        # check non arabic words in index
        non_arabic_words = [w for w in word_index if not araby.is_arabicword(w)]
        print("index size ",len(word_index))
        print("index size ",len(word_index.keys()))
        self.assertEqual(len(word_index.get("",[])), 0, " Index contains Empty words")  # add assertion here
        self.assertEqual(len(non_arabic_words), 0, " Index contains non Arabic word")  # add assertion here
        self.assertEqual(len(word_index), 3141, " Index size changed")  # add assertion here

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
        sm = self.db.get_all()
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


    # @unittest.skip("to do")
    def test_check_inflection(self):
        """
        test create index
        """
        sm = self.db.get_all()
        wrongs = []
        cpt = 0
        for id1 in sm:
            inflects_lines =  sm[id1]["inflection"].strip().split(".")
            # if len(inflects_lines)>=2  and inflects_lines[0].strip() == inflects_lines[1].strip():
            #     inflects_lines = inflects_lines[1:]
            warn = ""
            new_lines = []
            for i, line in enumerate(inflects_lines):
                line = line.strip()
                parts = line.split(":")
                part0 = parts[0]
                remain_parts = ":".join(parts[1:])
                if ":" in line:
                    if len(part0) > len(remain_parts):
                       if  (not line.startswith("وجملة")
                         and not line.startswith("والجملة")
                         and not line.startswith("وشبه الجملة")
                         and not line.startswith("والمصدر المؤول")
                         ):
                            warn = "Line '%d':key '%s' is too long"%(i, part0)
                            wrongs.append((id1, warn))
                elif not line:
                    pass
                elif (not line.startswith("وجملة")
                      and not line.startswith("والجملة")
                      and not line.startswith("وشبه الجملة")
                      and not line.startswith("والمصدر المؤول")
                ):
                    warn = " Line %d: start error [%s]" %(i,line)
                    wrongs.append((id1, warn))
                    line = "TOJOIN"+line
                else:
                    pass
                    # line = "###" +line
                new_lines.append(line)
                text  = ".\n".join(new_lines)
                # join lines
                text = text.replace(".\nTOJOIN", "")
                sm[id1]["inflection"] = text
            # pprint.pprint(new_lines)

        pprint.pprint(wrongs)
        # pprint.pprint(sm, width=500)
        # print(sm)
        self.assertEqual(len(wrongs), 0, "There are wrong lines inflection")  # add assertion here

    def test_get_all(self):
        """
        test create index
        """
        results = self.db.get_all()
        pprint.pprint(results)
        # pprint.pprint(sm, width=500)
        # print(sm)
        self.assertEqual(len(results), 1268, "There are wrong lines inflection")

    @unittest.skip("Done")
    def test_load_samples_data(self):
        """
        test create index
        """
        self.db.load_samples_data()
        results = self.db.get_all()
        pprint.pprint(results)
        # pprint.pprint(sm, width=500)
        # print(sm)
        self.assertEqual(len(results), 100, "Error on loading samples data")

    def test_get_by_id(self):
        """
        test create index
        """
        id = 251
        row = self.db.get_by_id(id)
        pprint.pprint(row)
        # pprint.pprint(sm, width=500)
        # print(sm)
        self.assertEqual(row.get("phrase",""), "قرضتِ النملةُ رِجْلَ الصيادِ", " Get ID error")

if __name__ == '__main__':
    unittest.main()
