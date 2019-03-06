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
from tools.tools import dirhash

class Test(unittest.TestCase):
    def test_gzip(self):
        if os.path.exists("./tests/out/repo2data_gzip"):
            shutil.rmtree("./tests/out/repo2data_gzip")
        repo2data = Repo2Data("./tests/in/gzip.json")
        repo2data.install()
        self.assertEqual(dirhash("./tests/out/repo2data_gzip"), dirhash("./tests/out/gzip/repo2data_gzip"))