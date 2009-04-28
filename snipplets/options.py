# options.py
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
import cPickle

class Options(object):
    
    def __init__(self, home_dir):
        #check if the user has some options already
        self.options_file = os.path.join(home_dir, "options")
        if not os.path.exists(self.options_file):
            self.set_default_options()
            
    def set_default_options(self):
        self.options = {
            "dropbox_sync" : False,
            "dropbox_folder" : None
        }

    def load_options(self):
        f = open(self.options_file, "r")
        self.options = cPickle.load(f)
        f.close()
    
    def dump_options(self):
        f = open(self.options_file, "w")
        cPickle.dump(self.options, f)
        f.close()
        
