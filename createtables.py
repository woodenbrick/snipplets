# createtables.py
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
import time

#these are the default types for a setup of snipplets
types = [
    {"type" : "Code", "image" : "ui/images/binary.png", "encrypt_default" : 0},
    {"type" : "Command/Shortcut", "image" : "ui/images/terminal.png",
     "encrypt_default" : 0},
    {"type" : "Chat log", "image" : "ui/images/kdmconfig.png", "encrypt_default" : 0},
    {"type" : "Password/Key", "image" : "ui/images/password.png", "encrypt_default" : 1},
    {"type" : "Personal", "image" : "ui/images/user_male.png", "encrypt_default" : 1}
    ]

test_data = [
    {"description" : "Mommas fried chicken", "data" : "2 eggs, 1 chicken",
     "encryption" : 0, "type" : 2},
    {"description" : "Python code", "data" : "def Test():",
     "encryption" : 0, "type" : 1},
    {"description" : "GPG Key", "data" : "123123iojasdoij231",
     "encryption" : 0, "type" : 3}]

languages = ["texinfo", "octave", "sql", "latex", "cpp",
        "fortran", "markdown", "msil", "html", "lua", "vhdl", "diff",
        "haskell", "nemerle", "po", "perl", "java", "ini", "csharp",
        "css", "changelog", "python", "gtkrc", "c", "vbnet", "verilog",
        "javascript", "idl", "tcl", "R", "ada", "php", "pascal", "desktop",
        "makefile", "scheme", "ruby", "xml", "sh"]

tables = [
    """
    CREATE TABLE IF NOT EXISTS `snipplets` (
    `snippletid` INTEGER PRIMARY KEY,
    `typeid` int(6) NOT NULL,
    `description` varchar(255),
    `data` blob,
    `encryption` boolean DEFAULT 0,
    `language` int(2) DEFAULT 0,
    `modified` date NOT NULL)
    """,
    
    """
    CREATE TABLE IF NOT EXISTS `tags` (
    `tagid` int(8) NOT NULL,
    `name` varchar(50) NOT NULL,
    `count` int(5) NOT NULL,
    PRIMARY KEY (`tagid`))
    """,
    
    """
    CREATE TABLE IF NOT EXISTS `tagged` (
    `snippletid` INTEGER PRIMARY KEY,
    `tagid` int(8) NOT NULL)
    """,
    
    """
    CREATE TABLE IF NOT EXISTS `types` (
    `typeid` INTEGER PRIMARY KEY,
    `type` varchar(40) NOT NULL,
    `image` varchar(255),
    `encrypt_default` boolean DEFAULT 0)
    """,
    
    """CREATE TABLE IF NOT EXISTS `languages` (
    `language` varchar(30) NOT NULL,
    `lastused` date NOT NULL)
    """ 
    ]
