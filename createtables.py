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


tables = [
    """
    CREATE TABLE IF NOT EXISTS `snipplets` (
    `snippletid` int(8) NOT NULL,
    `type` varchar(30) NOT NULL,
    `description` varchar(255),
    `data` blob,
    `encryption` boolean DEFAULT 0,
    PRIMARY KEY (`snippletid`))
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
    `snippletid int(8) NOT NULL,
    tagid int(8) NOT NULL)
    """
    ]