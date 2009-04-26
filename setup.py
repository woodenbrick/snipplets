#!/usr/bin/python


from distutils.core import setup
import os
import glob 

PROGRAM_NAME = 'snipplets'
VERSION = '0.05'

glade  = glob.glob(os.path.join(os.getcwd(), "snipplets", "ui", "glade", "*.glade"))
images = glob.glob(os.path.join(os.getcwd(), "snipplets", "ui", "images", "*.png"))
syntax_files = glob.glob(os.path.join(os.getcwd(), "snipplets", "codebuffer",
                                      "syntax", "*.xml"))
desc = """Organise your snipplets of data"""

long_desc = """Long Desc"""
setup ( name = PROGRAM_NAME,
        version = VERSION,
        description = desc,
        long_description = long_desc,
        author = 'Daniel Woodhouse',
        author_email = 'wodemoneke@gmail.com',
	    license = 'GPLv3',
        platforms = ['Linux'],
        url = 'http://github.com/woodenbrick/snipplets',
        packages = ['snipplets', 'snipplets/codebuffer'],
        data_files = [
            ('share/applications/', ['extras/snipplets.desktop']),  
            ('share/snipplets/glade', glade),
            ('share/snipplets/images', images),
            ('bin/', ['bin/snipplets']),
            ('share/snipplets/syntax', syntax_files)
        ])
