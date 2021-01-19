#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# File: gpx.py
# Project: gpx2cvs
# Created Date: Monday, January 4th 2021, 11:03:56 am
# Author: Fabio Zito
# -----
# Last Modified: Tue Jan 19 2021
# Modified By: Fabio Zito
# -----
# MIT License
# 
# Copyright (c) 2021 ZF zitelog@gmail.com
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of
# this software and associated documentation files (the "Software"), to deal in
# the Software without restriction, including without limitation the rights to
# use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
# of the Software, and to permit persons to whom the Software is furnished to do
# so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# -----
# HISTORY:
# Date      	By	Comments
# ----------	---	----------------------------------------------------------
###### 

import re
import xml.dom.minidom
from datetime import datetime
from config.global_settings import DEBUG


class GPX:
    """Parse gpx file."""

    def __init__(self, file, options):
        """
        In version 1.0 parsing just <trkpt> tagname.
        The result is stored in self.result with the default columns:
        [latitude, longitude, time, date, hour, time_zone, speed, ele, sat, hdop]


        doc (XML DOM) -- document parsed from xml.dom.minidom.

        options (dictonary) -- is a list of user choices to parse element.
            -> stopping-time (int)    -- possible value in seconds eg. 600
            -> speed-range (tuple)    -- min and max value in km/h eg. (0, 5)
            -> distance-range (tuple) -- min and max value in km eg. (0, 5)
            -> output-type (string)   -- format that parsing results are saved (default csv) 
        """
        self.result = {'parser-type':'gpx'}

        doc = xml.dom.minidom.parse(file)
        points = doc.getElementsByTagName("trkpt")
        
        output_type = 'default'
        rows = []
    
        stopping_time = None
        speed_range = None
        distance_range = None
        
        

        if len(options):
            if options.get('stopping-time'):
                stopping_time = options.get('stopping-time')

            if options.get('speed-range'):
                speed_range = options.get('speed-range')

            if options.get('distance-range'):
                distance_range = options.get('distance-range')

        for point in points:
            row = None
            latitude = point.getAttribute("lat")
            longitude = point.getAttribute("lon")
            time = point.getElementsByTagName("time")[0].firstChild.nodeValue
            date = re.match(r'^(.*)T', time).group(1)
            hour = re.match(r'.*T(.*)\.', time).group(1)
            time_zone = re.match(r'.*\.(.*)$', time).group(1)
            speed = int(point.getElementsByTagName("speed")[0].firstChild.nodeValue)
            ele = point.getElementsByTagName("ele")[0].firstChild.nodeValue
            sat = point.getElementsByTagName("sat")[0].firstChild.nodeValue
            hdop = point.getElementsByTagName("hdop")[0].firstChild.nodeValue

            #The standard output will be these rows which contain all fields
            rows.append([latitude, longitude, time, date, hour, time_zone, speed, ele, sat, hdop]) 

        if stopping_time is not None and speed_range is not None:

            filter_rows = self.__filter_rows_from_time_speed_distance(rows, stopping_time, speed_range, distance_range)
            if len(filter_rows) > 0: #The new output will be the filtered rows
                rows.clear()
                rows = filter_rows.copy()
                filter_rows.clear()
                output_type = 'filtered'
        
        self.result['output_type'] = output_type
        self.result['rows'] = rows

           
    def __filter_rows_from_time_speed_distance(self, rows, stopping_time, speed_range, distance_range):
        """
        In version 1.0 filtered just from stopping_time and speed_range. 
        An algorithm has not yet been defined for the distance_range.

        The result is stored in self.rows with the filter columns:
        *       Start stopping info     *       End stopping info        *    
        *-------------------------------*--------------------------------*
        *                               *                                *
        [latitude, longitude, date, hour, latitude, longitude, date, hour, stopping_duration]

        stopping_time (int)  -- is the value (in seconds) of how long a 
                                stopover should lasts for the vehicle or 
                                the user to be considered unmoving, eg. 
                                a car in the traffic makes many stops 
                                (generally short) and therefore cannot 
                                be considered parked.
                                *You must use it together with the speed_range

        speed_range (tuple)  -- is the value (in km/h) to consider the vehicle or the user
                                unmoving. 
                                *You must use it together with the stopping_time
        
        distance_range (tuple) -- is the value (in km/h) to consider the vehicle or the user
                               unmoving. 
                               *#TO-DO an algorithm has not yet been defined for the distance_range
        """

        find_it = False
        start_time = 0
        end_time = 0
        canditate_row = None
        seconds_in_minute = 60
        filter_rows = []

        min_speed, max_speed = speed_range

        max_speed += 1 #Increment of 1 because range doesn't consider last value

        last_row = len(rows)
        counter = 1

        for row in rows:

            latitude  = row[0]
            longitude = row[1]
            time      = row[2]
            date      = row[3]
            hour      = row[4]
            speed     = row[6]
            
            format_date = datetime.strptime(time, '%Y-%m-%dT%H:%M:%S.%f%z')

            if speed in range(min_speed, max_speed) and find_it == False:
                find_it = True
            elif speed not in range(min_speed, max_speed) and find_it == True:
                find_it = False

            if find_it == True:
                if start_time == 0:
                    start_time = format_date.timestamp() #Convert time in unix epoch
                    canditate_row = [latitude, longitude, date, hour] #fields correspond to begin of stopover

                end_time = format_date.timestamp()
                seconds = end_time - start_time

                if seconds >= stopping_time:
                    minutes = seconds / seconds_in_minute
                    seconds = seconds - (minutes * seconds_in_minute)
                    stopping_duration = f"{minutes}:{seconds}"
                    del canditate_row[4:] #remove all element affter the first four 
                    canditate_row.extend([latitude, longitude, date, hour, round(minutes)]) #fields correspond to the end of stopover
            else:
                start_time = 0
                end_time = 0

                if len(canditate_row) > 4:
                    filter_rows.append(canditate_row.copy())
                    canditate_row.clear()

            counter += 1

            if last_row == counter:
                if len(canditate_row) > 4:
                    filter_rows.append(canditate_row.copy())
                    canditate_row.clear()


        if distance_range is not None:
            pass #TO-DO Define how to implement the distance filter

        return filter_rows

    def get_result(self):
        return self.result