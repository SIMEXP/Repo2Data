#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 15:58:07 2019

@author: ltetrel
"""

import unittest
import shutil
import os
import json
from repo2data.repo2data import Repo2Data

class Test(unittest.TestCase):
    def test_s3(self):
        data_req_path = "./tests/in/s3.json"
        with open(data_req_path, "r") as f:
            data_req = json.load(f)
        dir_path = os.path.join(data_req["dst"], data_req["projectName"])
        if os.path.exists(dir_path):
            shutil.rmtree(dir_path)
            
        repo2data = Repo2Data(data_req_path)
        repo2data.install()
        dirs = os.listdir(dir_path)
        self.assertTrue(len(dirs) > 1)