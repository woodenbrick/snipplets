# syntaxhighlight.py
#
# Copyright 2009 Daniel Woodhouse
#
#This file is part of snipplets.
#
#snipplets is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#snipplets is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with snipplets.  If not, see http://www.gnu.org/licenses/

from gtkcodebuffer import CodeBuffer, SyntaxLoader
import dbsnipplet

class HighLighter(object):
    def __init__(self, db):
        self.db = db
        self.filetypes = []
        lang = self.db.query("""SELECT language from languages ORDER BY
                                       lastused DESC""")
        for l in lang:
            self.filetypes.append(l[0])


    def set_buffer_language(self, syntax_chosen):
        """Returns a buffer set to the correct language"""
        if syntax_chosen < 0:
            syntax_chosen = 2
        lang = SyntaxLoader(self.filetypes[syntax_chosen])
        buffer = CodeBuffer(lang=lang)
        return buffer

                 

