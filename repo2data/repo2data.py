#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 11:55:12 2018

@author: ltetrel
"""
import os
import json
import wget
import subprocess
import urllib
import patoolib
import datalad.api as datalad

class Repo2Data():

    def __init__(self, data_requirement=None):
        self._data_requirement_path = None
        self._data_requirement_file = None
        self._dst_path = None

        self.set_data_requirement_path(data_requirement)

    def get_data_requirement_path(self):
        return self._data_requirement_path

    def set_data_requirement_path(self, data_requirement_path):
        if data_requirement_path is None:
            self._data_requirement_path = os.path.join(os.getcwd(), "data_requirement.json")
        else:
            self._data_requirement_path = data_requirement_path
        
        self._update_data_requirement_file()
        self._dst_path = os.path.join(self._data_requirement_file["dst"]
                                    , self._data_requirement_file["projectName"])
        
    def _update_data_requirement_file(self):
        with open(self._data_requirement_path, 'r') as fst:
            self._data_requirement_file = json.load(fst)
            
    def _archive_decompress(self):
        files = os.listdir(self._dst_path)
        for file in files:
            try:
                patoolib.extract_archive(os.path.join(self._dst_path, file)
                                        , outdir=self._dst_path
                                        , verbosity=-1
                                        , interactive=False)
                print("Info : %s Decompressed" %(file))
            except patoolib.util.PatoolError:
                print("Info : %s is not an archive or not compatible with patoolib \
                      , bypassing decompression..." %(file))
        
    def _already_downloaded(self):
        # The configuration file was saved if the data was correctly downloaded
        if not os.path.exists( os.path.join(self._dst_path, "data_requirement.json")):
            if not os.path.exists(self._dst_path):
                os.mkdir(self._dst_path)
            dl = False
        else:
            dl = True
            
        return dl
        
    def install(self):
        if not self._already_downloaded():
            print("Info : Starting to download %s ..." %(self._data_requirement_file["src"]))
            # Try it few times to avoid truncated data
            attempts = 0
            while attempts < 3:
                #1. Download with standard weblink
                try:
                    wget.download(self._data_requirement_file["src"]
                                 , out=self._dst_path)
                    print(" ")
                    attempts = 999
                except urllib.error.ContentTooShortError:
                    attempts = attempts + 1
                    print("Warning : Truncated data, retry %d ..." %(attempts))
            
#            #2. Using datalad
#            datalad.install(path=self._data_requirement_file["dst"]
#                            ,source=self._data_requirement_file["src"]
#                            ,get_data=True
#                            ,recursive=self._data_requirement_file["recursive"])
#            #3. With s3
#            try:
#                subprocess.check_call(['aws s3 sync --no-sign-request'
#                                       , self._data_requirement_file["src"]
#                                       , self._data_requirement_file["dst"]])
#            except FileNotFoundError:
#                print("aws does not appear to be installed")
            
            # If needed, decompression of the data
            self._archive_decompress()
            
            # Finally, we write the data_requirement.json in the output folder
            # to avoid redownloading the same data in the future if it exists
            ###### Different behaviour if datalad update ???
            with open( os.path.join(self._dst_path, "data_requirement.json"), 'w') as fst:
                json.dump(self._data_requirement_file, fst)
            
        else:
            print('Info : %s already downloaded' %(self._dst_path))
    
if __name__ == '__main__':
    repo2Data = Repo2Data("/home/ltetrel/Documents/work/Repo2Data/examples/data_requirement.json")
    repo2Data.install()
