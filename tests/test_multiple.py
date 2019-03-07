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
    def test_multiple(self):
        if os.path.exists("./tests/out/repo2data_multiple1"):
            shutil.rmtree("./tests/out/repo2data_multiple1")
        if os.path.exists("./tests/out/repo2data_multiple2"):
            shutil.rmtree("./tests/out/repo2data_multiple2")
        repo2data = Repo2Data("./tests/in/multiple.json")
        repo2data.install()
        self.assertTrue(os.path.exists("./tests/out/repo2data_multiple1/AUTHORS"))
        self.assertTrue(os.path.exists("./tests/out/repo2data_multiple1/data_requirement.json"))
        self.assertTrue(os.path.exists("./tests/out/repo2data_multiple2/LICENSE"))
        self.assertTrue(os.path.exists("./tests/out/repo2data_multiple2/data_requirement.json"))
