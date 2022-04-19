#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  6 15:58:07 2019

@author: ltetrel
"""

import unittest
import shutil
import os
from repo2data.repo2data import Repo2Data

class Test(unittest.TestCase):
    def test_neurolibre_layout(self):
        data_req_path = "./tests/in/neurolibre/binder/neurolibre_layout.json"
        if os.path.exists("./tests/in/neurolibre/data/repo2data_neurolibre_layout"):
            shutil.rmtree("./tests/in/neurolibre/data/repo2data_neurolibre_layout")
        repo2data = Repo2Data(data_req_path)
        data_path = repo2data.install()[0]
        print(data_path)
        self.assertTrue(len(os.listdir(data_path)) > 1)
