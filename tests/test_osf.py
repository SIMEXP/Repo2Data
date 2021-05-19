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
    def test_osf(self):
        if os.path.exists("./tests/out/repo2data_osf"):
            shutil.rmtree("./tests/out/repo2data_osf")
        repo2data = Repo2Data("./tests/in/osf.json")
        repo2data.install()