#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  24 13:01:08 2020

@author: ltetrel
"""

import unittest
import shutil
import os
from repo2data.repo2data import Repo2Data

class Test(unittest.TestCase):
    def test_url(self):
        if os.path.exists("./data/repo2data_s3_binder"):
            shutil.rmtree("./data/repo2data_s3_binder")
        repo2data = Repo2Data("https://github.com/ltetrel/repo2data-caching-s3")
        repo2data.install()
        # disabling assertion because some uuids are differents