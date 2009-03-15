# dbsnipplet.py
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

import os
import sqlite3


class DbSnipplet(object):
    
    def __init__(self, database):
        print database
        if not os.path.exists(database):
            
            self.db, self.cursor = self.create_new_database(database)
        else:
            self.db = sqlite3.Connection(database)
            
    
    def create_new_database(self, database):
        db = sqlite3.Connection(database)
        cursor = db.cursor()
        import createtables
        for query in createtables.tables:
            cursor.execute(query)
        cursor.executemany("""INSERT INTO types (type, image, encrypt_default)
                           VALUES (:type, :image, :encrypt_default)""", createtables.types)
        db.commit()

        return db, cursor
    
    
    
    def return_types(self):
        pass
    
    
    
    def add_new(self):
        pass
    
    
    
    def delete(self):
        pass
    
    
    
    def edit(self):
        pass
