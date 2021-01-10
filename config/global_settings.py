#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# File: global_settings.py
# Project: gpx2cvs
# Created Date: Friday, January 8th 2021, 5:17:44 pm
# Author: Fabio Zito
# -----
# Last Modified: Sun Jan 10 2021
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

DEBUG = False

cvs_header = {}


#
#   *       Start stopping info     *       End stopping info        *    
#   *-------------------------------*--------------------------------*
#   *                               *                                *
#   [latitude, longitude, date, hour, latitude, longitude, date, hour, stopping_duration]
#
filtered_header = [
    'start_latitude','start_longitude','start_date','start_hour', #fileds correspond to begin of stopover
    'end_latitude','end_longitude','end_date','end_hour', #fields correspond to the end of stopover
    'stopping_duration (integer rounded minutes)'
]

default_header = [
    'latitude','longitude', 'time (original)','date','hour',
    'time_zone','speed','ele','sat','hdop'
]

#header for gpx parsing result
cvs_header['gpx'] = {'default': default_header, 'filtered': filtered_header}