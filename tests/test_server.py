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
    def test_server(self):
        if os.path.exists("/DATA/repo2data_server"):
            shutil.rmtree("/DATA/repo2data_server")
        repo2data = Repo2Data("./tests/in/server.json", True)
        repo2data.install()
        self.assertEqual(dirhash("/DATA/repo2data_server"), dirhash("./tests/out/server/repo2data_server"))
