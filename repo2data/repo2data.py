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
import urllib.request
import patoolib

class Repo2Data():
    def __init__(self, data_requirement=None, server=False):
        self._data_requirement_path = None
        self._data_requirement_file = None
        self._use_server = server
        
        self.load_data_requirement(data_requirement)

    def _set_data_requirement_path(self, data_requirement_path):
        if data_requirement_path is None:
            self._data_requirement_path = os.path.join(os.getcwd(), "data_requirement.json")
        else:
            self._data_requirement_path = data_requirement_path
        
        self._update_data_requirement_file()
        
    def _update_data_requirement_file(self):
        # Check if data_requirement is a github link
        if re.match(".*?(github\\.com).*?", self._data_requirement_path):
            try:
                orga_repo = re.match(".*?github\\.com(/.*/.*)", self._data_requirement_path)[1]
                raw_url = "https://raw.githubusercontent.com%s/HEAD/data_requirement.json" %(orga_repo)
                with urllib.request.urlopen(raw_url) as url:
                    self._data_requirement_file = json.loads(url.read().decode())
            # if requirement file is not in root repo, we check under binder directory
            except:
                try:
                    raw_url = "https://raw.githubusercontent.com%s/HEAD/binder/data_requirement.json" %(orga_repo)
                    with urllib.request.urlopen(raw_url) as url:
                        self._data_requirement_file = json.loads(url.read().decode())
                except:
                    raise Exception("{} does not contain a data_requirement.json file!".format(self._data_requirement_path))
        # else if it is indeed a req file
        elif re.match(".*?\\.json", self._data_requirement_path):
            with open(self._data_requirement_path, 'r') as fst:
                self._data_requirement_file = json.load(fst)
        else:
            raise Exception("{} is neither a valid url or filepath!".format(self._data_requirement_path))
        
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
                    Repo2DataChild(value, self._use_server).install()
        #if not, it is a single assignment
        else:
            Repo2DataChild(self._data_requirement_file, self._use_server).install()
            
        
class Repo2DataChild():
    def __init__(self, data_requirement_file=None, use_server=False):
        self._data_requirement_file = None
        self._dst_path = None
        self._use_server = use_server
        self._server_dst_folder = "./data"
        
        self.load_data_requirement(data_requirement_file)

    def load_data_requirement(self, data_requirement_file):
        # here we should load just a json data
        try:
            input = json.dumps(data_requirement_file)
            json.loads(input)
            self._data_requirement_file = data_requirement_file
        except TypeError:
            print("Could not load json data.")
            raise
        
        if(self._use_server):
            self._dst_path = os.path.join(self._server_dst_folder
                                        , self._data_requirement_file["projectName"])
        else:
            self._dst_path = os.path.join(self._data_requirement_file["dst"]
                                        , self._data_requirement_file["projectName"])
        
    def _archive_decompress(self):
        files = os.listdir(self._dst_path)
        for file in files:
            try:
                patoolib.extract_archive(os.path.join(self._dst_path, file)
                                        , outdir=self._dst_path
                                        , interactive=False)
                # now we can safely delete the archive
                if os.path.exists(os.path.join(self._dst_path, file)):
                    os.remove(os.path.join(self._dst_path, file))
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
        saved_req_path = os.path.join(self._dst_path, "data_requirement.json")
        # The configuration file was saved if the data was correctly downloaded
        if not os.path.exists(saved_req_path):
            dl = False
        else:
            # check content
            with open(saved_req_path, 'r') as f:
                saved_req = json.load(f)
            if self._data_requirement_file == saved_req:
                dl = True
            else:
                dl = False
            
        return dl
        
    def _wget_download(self):
        print("Info : Starting to download with wget %s ..." %(self._data_requirement_file["src"]))
        # Try it few times to avoid truncated data
        attempts = 0
        while attempts < 3:
            #Download with standard weblink
            try:
                wget.download(self._data_requirement_file["src"]
                             , out=self._dst_path)
                print(" ")
                attempts = 999
            except urllib.error.ContentTooShortError:
                attempts = attempts + 1
                print("Warning : Truncated data, retry %d ..." %(attempts))
                pass

    def _gdrive_download(self):
        print("Info : Starting to download from Google drive %s ..." %(self._data_requirement_file["src"]))
        try:
            # gdown does not allow to give output dir
            cwd = os.getcwd()
            os.chdir(self._dst_path)
            subprocess.check_call(['gdown'
                                   , self._data_requirement_file["src"]])
            os.chdir(cwd)
        except FileNotFoundError:
            print("Error: gdown does not appear to be installed")
            raise
    
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
            
    def _lib_download(self):
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

    def _osf_download(self):
        print("Info : Starting to download from osf {} ...".format(self._data_requirement_file["src"]))
        try:
            project_id = re.match("https://osf.io/(.{5})", self._data_requirement_file["src"])[1]
            subprocess.check_call(['osf'
                                   , '--project'
                                   , project_id
                                   , 'clone'
                                   , self._dst_path])
        except FileNotFoundError:
            print("Error: osf does not appear to be installed")
            raise
    
    def _scan_dl_type(self):
        # if it is an http link, then we use wget
        if ((re.match(".*?(https://).*?", self._data_requirement_file["src"])
                or re.match(".*?(http://).*?", self._data_requirement_file["src"]))
                and not re.match(".*?(\\.git)", self._data_requirement_file["src"])
                and not re.match(".*?(drive\\.google\\.com).*?", self._data_requirement_file["src"])
                and not re.match(".*?(https://osf\\.io).*?", self._data_requirement_file["src"])):
            self._wget_download()
        # if the source link has a .git, we use datalad
        elif re.match(".*?(\\.git)", self._data_requirement_file["src"]):
            self._datalad_download()
        # or coming from google drive
        elif re.match(".*?(drive\\.google\\.com).*?", self._data_requirement_file["src"]):
            self._gdrive_download()
        #or maybe it is a python script
        elif re.match(".*?(import.*?;).*?", self._data_requirement_file["src"]):
            self._lib_download()
        # or a s3 link ?
        elif re.match(".*?(s3://).*?", self._data_requirement_file["src"]):
            self._s3_download()
        # or osf
        elif re.match(".*?(https://osf.io).*?", self._data_requirement_file["src"]):
            self._osf_download()
    
    def install(self):
        print("Destination:")
        print(self._dst_path)
        print()
        
        if not self._already_downloaded():
            if not os.path.exists(self._dst_path):
                os.makedirs(self._dst_path)
            # Downloading with the right method, depending on the src type
            self._scan_dl_type()
            # If needed, decompression of the data
            self._archive_decompress()
            
            # Finally, we write the data_requirement.json in the output folder
            # to avoid redownloading the same data in the future if it exists
            #TODO: How to manage datalad update
            with open( os.path.join(self._dst_path, "data_requirement.json"), 'w') as fst:
                json.dump(self._data_requirement_file, fst)
        else:
            print('Info : %s already downloaded' %(self._dst_path))

        return self._dst_path
