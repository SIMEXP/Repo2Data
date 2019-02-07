#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 11:55:12 2018

@author: ltetrel
"""
import os
import json
import numpy as np

class Repo2Data():

    def __init__(self, data_requirement_path=None):
        self._data_requirement_path = None
        self._data_requirement_file = None

        self.set_data_requirement_path(data_requirement_path)
        self._set_data_requirement_file()

    def get_data_requirement_path(self):
        return self._data_requirement_path

    def set_data_requirement_path(self, data_requirement_path):
        if data_requirement_path is None:
            self._data_requirement_path = os.path.join(os.getcwd(), "data_requirement.json")
        else:
            self._data_requirement_path = data_requirement_path

        self._data_requirement_path = json.load(self._data_dir)
        
    def _set_data_requirement_file(self):
        with open(self._data_requirement_path, 'r') as fst:
            self._data_requirement_file = json.load(fst)
