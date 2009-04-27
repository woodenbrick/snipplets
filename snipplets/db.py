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
        if not os.path.exists(database):
            self.db, self.cursor = self.create_new_database(database)
        else:
            self.db = sqlite3.Connection(database)
            self.cursor = self.db.cursor()
            
    
    def create_new_database(self, database):
        db = sqlite3.Connection(database)
        cursor = db.cursor()
        import createtables
        for query in createtables.tables:
            cursor.execute(query)
        cursor.executemany("""INSERT INTO types (type, encrypt_default)
                           VALUES (:type, :encrypt_default)""",
                           createtables.types)
        cursor.executemany("""INSERT INTO snipplets (typeid, description, data,
                           encryption, language, modified) VALUES (:type, :description,
                           :data, :encryption, :language, datetime('now', 'localtime'))""",
                           createtables.test_data)
        for language in createtables.languages:
            cursor.execute("""INSERT INTO languages (language, lastused) VALUES
                               (?, datetime('now', 'localtime'))""", (language,))
        db.commit()

        return db, cursor
    
    
    def query(self, query):
        """executes query and returns all"""
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def return_all(self, table):
        query = "SELECT * FROM %s" % table
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    
    def return_most_recent_snipplet(self):
        self.cursor.execute("""select snipplets.snippletid, types.type,
                            snipplets.description, snipplets.modified,
                            snipplets.encryption FROM snipplets INNER JOIN types ON
                            snipplets.typeid=types.typeid ORDER BY snipplets.modified
                            desc LIMIT 1""")
        return self.cursor.fetchone()
    
    
    def return_snipplet_selection(self):
        """Retrieves snipplet info without data"""
        self.cursor.execute("""select snipplets.snippletid, types.type,
                            snipplets.description, snipplets.modified,
                            snipplets.encryption FROM snipplets INNER JOIN types ON
                            snipplets.typeid=types.typeid ORDER BY snipplets.modified desc""")
        return self.cursor.fetchall()
    
    
    def return_snipplet_data(self, id=None):
        """Retrieves the data for snipplet with this id or all"""
        if id is None:
            self.cursor.execute("""select data, typeid, description, encryption, language, modified
                            from snipplets""")
            return self.cursor.fetchall()
        self.cursor.execute("""select data, typeid, description, encryption, language, modified
                            from snipplets where snippletid=?""", (id,))
        
        return self.cursor.fetchone()
    

    
    
    def add_new(self, snipplet_obj):
        self.cursor.execute("""INSERT INTO snipplets (typeid, description,
                            data, encryption, language, modified) VALUES (:type, :description, :data,
                            :encryption, :language, datetime('now', 'localtime'))""",
                            snipplet_obj)
        self.db.commit()
    
    
    
    def delete(self, id):
        self.cursor.execute("""DELETE FROM snipplets WHERE snippletid=?""", (id,))
        self.db.commit()
    
    
    
    def edit(self, snipplet_obj):
        self.cursor.execute("""UPDATE snipplets set typeid=:type,
                            description=:description, data=:data,
                            encryption=:encryption, language=:language,
                            modified=datetime('now', 'localtime')
                            where snippletid=:snippletid""", snipplet_obj)
        self.db.commit()
        
        

            
