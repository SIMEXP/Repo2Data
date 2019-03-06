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
import re
import urllib
import patoolib

class Repo2Data():
    def __init__(self, data_requirement=None):
        self._data_requirement_path = None
        self._data_requirement_file = None
        
        self.load_data_requirement(data_requirement)

    def _set_data_requirement_path(self, data_requirement_path):
        if data_requirement_path is None:
            self._data_requirement_path = os.path.join(os.getcwd(), "data_requirement.json")
        else:
            self._data_requirement_path = data_requirement_path
        
        self._update_data_requirement_file()
        
    def _update_data_requirement_file(self):
        with open(self._data_requirement_path, 'r') as fst:
            self._data_requirement_file = json.load(fst)
        
    def load_data_requirement(self, data_requirement):
        # we try if data_requirement is a str
        if isinstance(data_requirement, str) or data_requirement is None:
            self._set_data_requirement_path(data_requirement)
            
    def install(self):
        print("---- repo2data starting ----")
        print(os.path.dirname(__file__))
        print("Config from file :")
        print(self._data_requirement_path)
        
        #Here we check if the first item is a dict (mutiple requirement)
        if isinstance(self._data_requirement_file[ next(iter(self._data_requirement_file)) ], dict):
            for key, value in self._data_requirement_file.items():
                if isinstance(value, dict):
                    Repo2DataChild(value, self._data_requirement_path).install()
        #if not, it is a single assignment
        else:
            Repo2DataChild(self._data_requirement_file, self._data_requirement_path).install()
            
        
class Repo2DataChild():
    def __init__(self, data_requirement_file=None, data_requirement_path=None):
        self._data_requirement_path = None
        self._data_requirement_file = None
        self._dst_path = None
        
        self.load_data_requirement(data_requirement_file)
        self._set_data_requirement_path(data_requirement_path)

    def get_data_requirement_path(self):
        return self._data_requirement_path

    def _set_data_requirement_path(self, data_requirement_path):
        self._data_requirement_path = data_requirement_path

    def load_data_requirement(self, data_requirement_file):
        # here we should load just a json data
        try:
            input = json.dumps(data_requirement_file)
            json.loads(input)
            self._data_requirement_file = data_requirement_file
        except TypeError:
            print("Could not load json data.")
            raise
        
        self._dst_path = os.path.join(self._data_requirement_file["dst"]
                                    , self._data_requirement_file["projectName"])
        
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
                # we want to print the list of available formt JUST if the file is indeed an archive
                try:
                    patoolib.get_archive_format(os.path.join(self._dst_path, file))
                    print("Info : %s is not compatible with patoolib " \
                          ", bypassing decompression..." %(file))
                    list_formats = str(patoolib.list_formats())
                    print("Info: available archive formats :" + list_formats)
                except patoolib.util.PatoolError:
                    pass
        
    def _already_downloaded(self):
        # The configuration file was saved if the data was correctly downloaded
        if not os.path.exists( os.path.join(self._dst_path, "data_requirement.json")):
            if not os.path.exists(self._dst_path):
                os.mkdir(self._dst_path)
            dl = False
        else:
            dl = True
            
        return dl
        
    def _wget_download(self):
        print("Info : Starting to download with wget %s ..." %(self._data_requirement_file["src"]))
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
                pass
    
    def _datalad_download(self):
        print("Info : Starting to download from datalad %s ..." %(self._data_requirement_file["src"]))
        try:
            subprocess.check_call(['datalad'
                                   , 'install'
                                   , self._dst_path
                                   , "-s"
                                   , self._data_requirement_file["src"]])
        except FileNotFoundError:
            print("Error: datalad does not appear to be installed")
            raise
            
    def _cmd_download(self):
        str_cmd = self._data_requirement_file["src"]
        str_cmd = str_cmd.replace("_dst", "\"" + self._dst_path + "\"")
        print("Info : Starting to download from python lib %s ..." %(self._data_requirement_file["src"]))
        subprocess.check_call(["python3", "-c", str_cmd])
    
    def _s3_download(self):
        print("Info : Starting to download from s3 %s ..." %(self._data_requirement_file["src"]))
        try:
            subprocess.check_call(['aws'
                                   , 's3'
                                   , 'sync'
                                   , '--no-sign-request'
                                   , self._data_requirement_file["src"]
                                   , self._dst_path])
        except FileNotFoundError:
            print("Error: aws does not appear to be installed")
            raise
    
    def _scan_src(self):
        return False
    
    def install(self):
        print("Ouptut:")
        print(self._dst_path)
        print()
        
        if not self._already_downloaded():
            # if it is an http link, then we use wget
            if (re.match(".*?(https://).*?", self._data_requirement_file["src"])
                and not re.match(".*?(\.git)", self._data_requirement_file["src"])):
                self._wget_download()
                
            # if the source link has a .git, we use datalad
            elif re.match(".*?(\.git)", self._data_requirement_file["src"]):
                self._datalad_download()
                
            #or maybe it is a python script
            elif re.match(".*?(import.*?;).*?", self._data_requirement_file["src"]):
                self._cmd_download()
                
            # or a s3 link ?
            elif re.match(".*?(s3://).*?", self._data_requirement_file["src"]):
                self._s3_download()
            
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
    
    repo2Data = Repo2Data("/home/ltetrel/Documents/work/Repo2Data/examples/data_requirement_multiple.json")
    repo2Data.install()
    
    repo2Data = Repo2Data("/home/ltetrel/Documents/work/Repo2Data/examples/data_requirement_gzip.json")
    repo2Data.install()
    
    repo2Data = Repo2Data("/home/ltetrel/Documents/work/Repo2Data/examples/data_requirement_datalad.json")
    repo2Data.install()
    
    repo2Data = Repo2Data("/home/ltetrel/Documents/work/Repo2Data/examples/data_requirement_nilearn.json")
    repo2Data.install()
