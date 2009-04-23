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
    {"type" : "Code", "encrypt_default" : 0},
    {"type" : "Command", "encrypt_default" : 0},
    {"type" : "Key", "encrypt_default" : 1},
    {"type" : "Personal", "encrypt_default" : 1}
    ]

test_data = [
    {"description" : "Welcome to Snipplets!", "data" : """Snipplets is an easy way to keep
     your little snippets of data in order.""",
     "encryption" : 0, "type" : 2},
    {"description" : "Sample python code", "data" : """
     def Test():
         if x == 1:
             print x
            """,
     "encryption" : 0, "type" : 1, "language" : 21 },
    {"description" : "Snipplets PPA Public Key", "data" : """
-----BEGIN PGP PUBLIC KEY BLOCK-----
Version: SKS 1.0.10

mI0ESdosRwEEAPpNSzctKOn1Abu68iItXRtGCoFAU76Un1tS3eR7VePwXymrz94u9pGdxJ7z
1tBJcbYmXj4mbUUTIy21Itk9xdGwkZMqLgq7ejFdt1FLIHN9uVZmpx1V301ycC7I2qh7w0XI
3v7eQ8ovWJQ6M+EBt1qbXI9VpNANo+SbVizxWCmFABEBAAG0G0xhdW5jaHBhZCBQUEEgZm9y
IFNuaXBwbGV0c4i2BBMBAgAgBQJJ2ixHAhsDBgsJCAcDAgQVAggDBBYCAwECHgECF4AACgkQ
hAKD0aAcifVqkwP+IMJeawsgjDwxfxgHdttVIxrfYTy5Jwpwqs6DCD5bmg3L8r8jENloFNwv
VI5yZRcSPOSsCMXJntxJk+BYCLl1XHn3T1rHypi8tfaK40oU3jpVcLL1j5P4jlFMqVqLDhqu
yFSqKukRMIoO2GGBPzahwsZGpJiF4DGitTQtsj6PSxo=
=sh8m
-----END PGP PUBLIC KEY BLOCK-----""",
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
    `encrypt_default` boolean DEFAULT 0)
    """,
    
    """CREATE TABLE IF NOT EXISTS `languages` (
    `language` varchar(30) NOT NULL,
    `lastused` date NOT NULL)
    """ 
    ]
