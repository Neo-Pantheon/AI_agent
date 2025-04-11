#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  2 13:12:19 2025

@author: jaykim
"""

from llama_parse import LlamaParse
import os

os.environ["LLAMA_CLOUD_API_KEY"] = "xxxxxxxxxxx"

parsingInstruction = """You are provided with an expense report. Extract as table with Time, Duration, Status, Remark, Vehicle,  Odometer, Location in the table"""


vanilaParsing = LlamaParse(result_type='markdown', parsing_instruction=parsingInstruction).load_data('/workspace/FleetSamsara2.pdf')


print(vanilaParsing[0].text)
