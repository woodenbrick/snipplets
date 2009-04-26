# types.py
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

class Types(object):
    
    def __init__(self, type_data):
        self.types = []
        #type_data layout = (1, u'Code', u'ui/images/binary.png', 0)
        for row in type_data:
            self.types.append(row)
            

    
    def return_image_from_id(self, id):
        for row in self.types:
            if row[0] == id:
                return row[2]
        return False
    
    def return_image_from_name(self, name):
        pass
    
    
    
class Tags(object):
    
    def __init__(self, tag_data):
        pass