#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  samplesdb_factory.py
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

from . import samplesdb
from . import samplesdb_sql

class SamplesDB_factory:

    def __init__(self):
        pass

    @staticmethod
    def factory(samples_type, options=None):
        """
        return an object accrodngi to samples_type
        """
        if samples_type == "python":
            return samplesdb.SamplesDB()
        elif samples_type == "sqlite":
            return samplesdb_sql.SamplesDB_SQL()
        else:
            return samplesdb.SamplesDB()

def main():
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
