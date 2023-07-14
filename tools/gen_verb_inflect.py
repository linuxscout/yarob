#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# gen_verb_inflect.py
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
# Convert verb inflection Data to 
# a suitable for mysam verb inflection
# used in tag_const
import sys
import pprint
DATA_FILE = "../data-source/verbs.csv"

def treat_lines(lines):
    """
    Print lines into dict of verb 
    The data will be organized as
    
    {"tense":{"pronoun":{case fields},},
    }
    """
    list_fields = {}
    for line in lines:
        if not line.startswith("#"):
            line = line.strip("\n")
            fields = line.split("\t")
            if len(fields)>= 9:
                tense_code = fields[0]
                tense_arabic = fields[1]
                if not tense_arabic in list_fields:
                    list_fields[tense_arabic] = {} 
                pronoun = fields[2]
                inflect_dict= {
                'desciption': fields[3],
                "case" : fields[4],
                "case_weak" : fields[5],
                "cause" : fields[6],
                "subject" : fields[7],
                "extra": fields[8],
                }

                list_fields[tense_arabic][pronoun]= inflect_dict
            
    return list_fields
    
def main(args):
    
    filename = DATA_FILE
    try:
        fl = open(filename, encoding="utf-8")
    except:
        print("Error: Can't open file ", filename)
        sys.exit()
    else:
        lines = fl.readlines()
        data_structure = treat_lines(lines)
        print("TABLE_TENSE_PRONOUN_INFLECTION=", end="")
        pprint.pprint(data_structure)
    
    
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
