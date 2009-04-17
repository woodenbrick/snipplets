# misc.py
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

def nicetime(past_time, fuzzy=True, length=2):
    """Takes time in the form of 2009-12-04 14:55:02 and
    returns a nicely formatted string 2 hours ago...etc.
    fuzzy will leave todays times as Today <time>"""
    
    past_time = time.strptime(past_time, "%Y-%m-%d %H:%M:%S")
    ptime = str(past_time[3]) + ":" + str(past_time[4])
    current_time = time.localtime()
    
    strings = ["year", "month", "day"]
    if not fuzzy:
        strings.extend(["hour", "minute", "second"])
    
    sentence = []
    for i in range(0, len(strings)):
        diff = current_time[i] - past_time[i]
        #generate weeks
        if strings[i] == "day":
            weeks, diff = get_weeks(diff)
            if weeks > 0:
                plural = "" if weeks == 1 else "s"
                sentence.append(str(weeks) + " week" + plural)
        if diff <= 0:
            continue
        plural = "" if diff == 1 else "s"
        sentence.append(str(diff) + " " + strings[i] + plural)
    
    if len(sentence) > 0:
        return ", ".join(sentence[0:length]) + " ago, " + ptime
    return "Today, " + ptime


def get_weeks(days):
    weeks = int(days / 7)
    days = days % 7
    return weeks, days