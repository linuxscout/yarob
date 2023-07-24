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

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

from pyarabic import araby
import qalsadi.analex
import qalsadi.stemnode

from . import samplesdb


try:
    from . import samples_const
except:
    import samples_const


# engine = create_engine('sqlite:///sales.db', echo = True)
Base = declarative_base()

class Samples_base(Base):
    __tablename__ = 'samples_table'
    id = Column(Integer, primary_key=True)
    # phrase
    phrase = Column(String)
    unvocalized = Column(String)

    inflection = Column(Text)
    structured_inflection = Column(String)

    phrase_type = Column(String)
    source = Column(String)
    reference = Column(String)

    keywords = Column(String)

    state = Column(String)
    date = Column(String)


class Terms_base(Base):
   __tablename__ = 'terms_table'
   id = Column(Integer, primary_key=True)
   # phrase
   term = Column(String,)
   id_phrase = Column(Integer)


class SamplesDB_SQL(samplesdb.SamplesDB):
    """
    A class to handle Inflection Samples and Data bases
    """
    def __init__(self, path=""):
        engine = create_engine('sqlite://', echo=True)
        # self.data  = samples_const.SAMPLES
        # # self.data = samples_temp.SAMPLES
        self.analyzer = qalsadi.analex.Analex()
        # self.path = path
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.load_samples_data()
        self.index = self._build_index()

    def _build_index(self,):
        """

        """
        # word_index = self.create_index(self.get_all())

        # to do: add index to data base
        word_index = self.create_index(self.get_all())
        cpt = 1
        for tok in word_index:
            for idp in word_index[tok]:
                self.session.add(Terms_base(id=cpt, term=tok, id_phrase = idp))
                cpt +=1
        self.session.commit()
        return word_index

        filename = "yarob_samplesdb_sql_index.pickle"
        try:
            with open(filename, "rb") as pickfile:
                word_index = pickle.load(pickfile)
            print("log build index, load")
        except (OSError, IOError):
            word_index = self.create_index(self.get_all())
            with open(filename, "wb") as pickfile:
                pickle.dump(word_index,pickfile )
            print("log build index- dumps")
        return word_index

    def create_index(self, data={}):
        """
        Create index of words in samples,
        Can create an index for a given data
        can enbale or disable cache
        """
        if not data:
            data = self.get_all()
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
        candidates_doc = []
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
            data_inflect = self.get_by_id(cand_id)
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
        result_query = self.session.query(Samples_base).all()
        results = {}
        for row in result_query:
            res = row.__dict__
            if '_sa_instance_state' in res:
                del res['_sa_instance_state']
            results[res["id"]] = res
        return results

    def get_by_id(self,rec_id, options={}):
        """
        return Data by id
        """
        row = self.session.get(Samples_base, rec_id)
        result  = row.__dict__
        if '_sa_instance_state' in result:
            del result['_sa_instance_state']
        return result


    def _get_ids_from_index(self, tokens):
        """
        return all ids from word indexes
        """
        ids = []
        for tok in tokens:
            # ids.extend(self.index.get(tok, []))
            result = self.session.query(Terms_base).filter(Terms_base.term == tok)
            ids.extend([res.id_phrase for res in result])
        return ids

    def load_fake_data(self,):
        """
        Load fake data to test database
        """
        c1 = Samples_base(date='2023-07-16', id=248,
                          inflection='''يزهُو: فعلٌ مضارعٌ مرفوعٌ - لأنه لم يسبقهُ ناصبٌ ولا جازمٌ ولم يلحق بآخِرِهِ شيءٌ- وعلامةُ رفعهِ الضمة المقدرةُ على آخِرِهِ منعَ من ظهورِهَا الثقلُ.
                 الربيعُ فاعلٌ مرفوعٌ وعلامةُ رفعهِ الضمةُ الظاهرةُ على آخرِهِ -اسمٌ مفردٌ تظهرُ عليه الحركاتُ الثلاثُ-.
        بالثمارِ: الباءُ :حرفُ جرٍّ مبنيٌّ على الكسرِ.
        الثمارِ:: اسمٌ مجرورٌ بحرف الجرِّ"الباء" وعلامةُ جرِّهِ الكسرةُ الظاهِرَةُ على آخِرِهِ.
        ''',

                          phrase='يزهُو الربيعُ بالثمارِ',
                          reference='وب',
                          source='',
                          state='draft',
                          structured_inflection="[]",
                          phrase_type='',
                          unvocalized='يزهو الربيع بالثمار')
        self.session.add(c1)
        self.session.commit()
        list_samples = [Samples_base(
            date='2023-07-16',
            id=249,
            inflection='''قفزَ: فعلٌ ماضٍ مبنيٌّ على الفتحِ الظاهرِ على آخِرِهِ ، لا محلَّ لَهُ للإعرابِ.
        الحِصانُ: فاعلٌ مرفوعٌ وعلامةُ رفعهِ الضمةُ الظاهرةُ على آخرِهِ -اسمٌ مفردٌ تظهرُ عليه الحركاتُ الثلاثُ-.
        بالفارسِ: الباءُ :حرفُ جرٍّ مبنيٌّ على الكسرِ.
        الفارسِ: اسمٌ مجرورٌ بحرف الجرِّ"الباء" وعلامةُ جرِّهِ الكسرةُ الظاهِرَةُ على آخِرِهِ.
        ''',
            keywords='حصان:قفز:فارس:لحص',
            phrase='قفزَ الحِصانُ بالفارسِ',
            reference='وب',
            source='',
            state='draft',
            structured_inflection="[]",
            phrase_type='',
            unvocalized='قفز الحصان بالفارس',
        ),

            Samples_base(
                date='2023-07-16',
                id=250,
                inflection='''يجري: فعلٌ مضارعٌ مرفوعٌ - لأنه لم يسبقهُ ناصبٌ ولا جازمٌ ولم يلحق بآخِرِهِ شيءٌ- وعلامةُ رفعهِ الضمةُ المقدرةُ على آخِرِهِ منعَ منْ ظُهُورِها للثقلِ.
        الحِصانُ: فاعلٌ مرفوعٌ وعلامةُ رفعهِ الضمةُ الظاهرةُ على آخرهِ -اسمٌ مفردٌ تظهرُ عليهِ الحركاتُ الثلاثُ-.
        بقوةٍ: الباءُ :حرفُ جرٍّ مبنيٌّ على الكسرِ.
        قوةٍ: اسمٌ مجرورٌ بحرف الجرِّ"الباء" وعلامةُ جرِّهِ الكسرةُ الظاهِرَةُ على آخِرِهِ.
        ''',
                keywords='جرى:أجرى:حصان:قوة:لحص',
                phrase='يجري الحِصانُ بقوةٍ',
                reference='وب',
                source='',
                state='reviewed',
                structured_inflection="[]",
                phrase_type='',
                unvocalized='يجري الحصان بقوة',
            ),
            Samples_base(
                date='2023-07-16',
                id=251,
                inflection='''قرضَ: فعلٌ ماضٍ مبنيٌّ على الفتحِ الظاهرِ على آخِرِهِ ، لا محلَّ لَهُ للإعرابِ.
        التاءُ: تاءُ التأنيثِ الساكنةُ وكُسِرَتْ لتفادي التقاءِ الساكنينِ.
        وهي: حرفٌ و علامةٌ على التأنيثِ، تدلُّ على أنَّ الفاعلَ مؤنثٌ.
        النملةُ: فاعلٌ مرفوعٌ وعلامةُ رفعهِ الضمةُ الظاهرةُ على آخرهِ -اسمٌ مفردٌ تظهرُ عليهِ الحركاتُ الثلاثُ.
        رِجْلَ: مفعولٌ بِهِ منصوبٌ وعلامةُ نصبِهِ الفتحةُ الظاهِرةُ على آخِرِهِ، وهو مضافٌ.
        الصيادِ: مضافٌ إليهِ مجرورٌ وعلامةُ جرِّهِ الكسرةُ الظاهِرَةُ على آخِرِهِ.
        ''',
                keywords='نملة:نمل:قرض:رجل:صياد',
                phrase='قرضتِ النملةُ رِجْلَ الصيادِ',
                reference='وب',
                source='',
                state='draft',
                structured_inflection="[]",
                phrase_type='',
                unvocalized='قرضت النملة رجل الصياد',
            ),
        ]
        self.session.add_all(list_samples)

        self.session.commit()

    def load_samples_data(self,):
        """
        Load fake data to test database
        """
        data = samples_const.SAMPLES
        for x in data:
            if 'type' in data[x]:
                data[x]['phrase_type'] = data[x].get('type', data[x].get('phrase_type',''))
                del data[x]['type']
        list_samples = [Samples_base(**data[x]) for x in data]
        self.session.add_all(list_samples)
        self.session.commit()

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
        

def main():
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
