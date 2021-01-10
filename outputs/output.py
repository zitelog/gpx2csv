#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# File: output.py
# Project: gpx2cvs
# Created Date: Thursday, January 7th 2021, 3:59:52 pm
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

from . import csv
from config.global_settings import DEBUG

class Output:
    """Set correct ouput from default value (csv) or from user choose."""

    def __init__(self, parser_result, file, options):
        """
            parser_result (dictonary) -- parsing result.
            file (string) -- file to save ouput. Extention is set to output-type (default .csv).

            options (dictonary) -- is a list of user choices to parse element.
                -> stopping-time (int)    -- possible value in seconds eg. 600
                -> speed-range (tuple)    -- min and max value in km/h eg. (0, 5)
                -> distance-range (tuple) -- min and max value in km eg. (0, 5)
                -> output-type (string)   -- format that parsing results are saved (default csv)
        """
        self.output = None
        module_name = 'csv'

        #check if type of output is a user choices
        if len(options) and options.get('output-type'):
            module_name = self.options.get('output-type')
        
        #if format are in list the output was developed
        format = [ele for ele in ['csv'] if(ele in module_name)]
      
        if not bool(format):
            raise ModuleNotFoundError(f'The output module for this format {module_name} has not yet been developed\n\n')
        
        module = globals().get(module_name)
        class_ = getattr(module, module_name.upper())
        self.output = class_(parser_result, file, options)

    def save(self):
        return self.output.save()