#!/usr/bin/env python3
# -*- coding:utf-8 -*-
######
# File: gpx2csv.py
# Project: gpx2cvs
# Created Date: Friday, January 8th 2021, 9:46:31 am
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

import os, argparse, sys

import config.global_settings as config
from pathlib import Path

from parsers.parser import Parser
from outputs.output import Output

'''gpx2csv parser, script entry point.'''


if __name__ == '__main__':

    if sys.version_info[0] < 3:
        sys.exit('Python 3 or a more recent version is required.')


    argparse = argparse.ArgumentParser(prog='gpx2csv', description="Parse file and save the result in csv file with same name")
    argparse.add_argument("filetoparse", help="If no path is specified the file will be searched in the current directory")
    argparse.add_argument("--stopping-time", type=int, metavar='', 
                                    help="(integer) is the value (in seconds) of how long a \
                                        stopover should lasts for the vehicle or \
                                        the user to be considered unmoving, eg. \
                                        a car in the traffic makes many stops \
                                        (generally short) and therefore cannot \
                                        be considered parked.\
                                        *You must use it together with the speed-range\
                                        eg. --stopping-time 600 --speed-range 0 5"
                        )
    argparse.add_argument('--speed-range', metavar='', nargs=2, type=int,
                                help="Are min and max values (in km/h) to consider \
                                        the vehicle or the user unmoving.\
                                        *You must use it together with the stopping-time\
                                        eg. --stopping-time 600 --speed-range 0 5"
                        )
    argparse.add_argument('--output-path', metavar='', help="output directory, must exist. If no path is specified the file will be saved in the current directory")

    args = argparse.parse_args()

    required_together = ('stopping_time','speed_range')

    if not Path(args.filetoparse).is_file():
        print (argparse.prog + f": error: argument filetoparse: file not exist: '{args.filetoparse}'")
        exit()

    if args.stopping_time is not None and args.speed_range is None or args.stopping_time is None and args.speed_range is not None :
        print (argparse.prog + f": error: You must use --stopping-time and --speed-range together")
        exit()

    if args.output_path is not None and not Path(args.output_path).is_dir():
        print (argparse.prog + f": error: argument output-path: path not exist: '{args.output_path}'")
        exit()


    inputfile = args.filetoparse
    outputfile = os.path.splitext(os.path.basename(inputfile))[0]
    options = {}

    if args.output_path is not None:
        outputfile = args.output_path + '/' + outputfile
        
    if args.stopping_time is not None:
        options = {'stopping-time': args.stopping_time, 'speed-range': args.speed_range}

    parser = Parser(inputfile, options)
    output = Output(parser.get_result(), outputfile, options)
    output.save()