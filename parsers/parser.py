#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# File: parser.py
# Project: gpx2cvs
# Created Date: Thursday, January 7th 2021, 4:00:35 pm
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

import re
from . import gpx

from config.global_settings import DEBUG

class Parser:
   """Set correct parser from file extension"""

   def __init__(self, file, options):
      """
      file (string) -- file to parse.

      options (dictonary) -- is a list of user choices to parse element.
         -> stopping-time (int)    -- possible value in seconds eg. 600
         -> speed-range (tuple)    -- min and max value in km/h eg. (0, 5)
         -> distance-range (tuple) -- min and max value in km eg. (0, 5)
         -> output-type (string)   -- format that parsing results are saved (default csv)
      """
      self.parser = None
      module_name = None

      #if extension are in list the parser was developed
      extension = [ele for ele in ['.gpx'] if(ele in file)]
      
      if not bool(extension):
         raise ModuleNotFoundError(f'The parse module for this type of file has not yet been developed\n\n')

      module_name = extension[0].replace('.', '')

      #import dynamically parse's module from name and instance it
      module = globals().get(module_name)
      class_ = getattr(module, module_name.upper())
      self.parser = class_(file, options)
      

   def get_result(self):
      return self.parser.get_result()


