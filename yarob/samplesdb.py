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

import samples_const

class SamplesDB():
    """
    A class to handle Inflection Samples and Data bases
    """
    def __init__(self, path=""):
        
        self.data  = {}
        self.index = {}
        pass
        
    def create_index(self,):
        """
        Create index of words in samples
        """
        pass
    
    
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
        return self._fake_match(phrase)

    def _fake_lookup(self, phrase):
        """
        Look up for phrase in samples data, exact search.
        Used just for testing
        """ 
        return [{"phrase":phrase,
            "inflection": "إعراب الجملة",
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
