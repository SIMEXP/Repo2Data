#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 11:55:12 2018

@author: ltetrel
"""
import os
import json
import requests
import subprocess
import re
import urllib
import urllib.request
import patoolib
import time


class Repo2Data():
    """Repo2data mother class which get user (nested) requirement file and launch child processes"""

    def __init__(self, data_requirement=None, server=False):
        """Initialize the Repo2Data mother class.
            Parameters
            ----------
                data_requirement : string
                    path to the data requirement file or github repository
                server : bool
                    whether to force output directory (default: False)
        """
        self._data_requirement_path = None
        self._data_requirement_file = None
        self._use_server = server
        self._server_dst_folder = "./data"

        self.load_data_requirement(data_requirement)

    def set_server_dst_folder(self,directory):
        self._server_dst_folder = directory

    def _set_data_requirement_path(self, data_requirement_path):
        """Define path to the requirement file"""
        if data_requirement_path is None:
            self._data_requirement_path = os.path.join(
                os.getcwd(), "data_requirement.json")
        else:
            self._data_requirement_path = data_requirement_path

        self._update_data_requirement_file()

    def _update_data_requirement_file(self):
        """Update data requirement if remote github url"""
        # Check if data_requirement is a github link
        if re.match(".*?(github\\.com).*?", self._data_requirement_path):
            try:
                orga_repo = re.match(
                    ".*?github\\.com(/.*/.*)", self._data_requirement_path)[1]
                raw_url = "https://raw.githubusercontent.com%s/HEAD/data_requirement.json" % (
                    orga_repo)
                with urllib.request.urlopen(raw_url) as url:
                    self._data_requirement_file = json.loads(
                        url.read().decode())
            # if requirement file is not in root repo, we check under binder directory
            except:
                try:
                    raw_url = "https://raw.githubusercontent.com%s/HEAD/binder/data_requirement.json" % (
                        orga_repo)
                    with urllib.request.urlopen(raw_url) as url:
                        self._data_requirement_file = json.loads(
                            url.read().decode())
                except:
                    raise Exception("{} does not contain a data_requirement.json file!".format(
                        self._data_requirement_path))
        # else if it is indeed a req file
        elif re.match(".*?\\.json", self._data_requirement_path):
            with open(self._data_requirement_path, 'r') as fst:
                self._data_requirement_file = json.load(fst)
        else:
            raise Exception("{} is neither a valid url or filepath!".format(
                self._data_requirement_path))

    def load_data_requirement(self, data_requirement):
        """Load data requirement file as json"""
        # we try if data_requirement is a str
        if isinstance(data_requirement, str) or data_requirement is None:
            self._set_data_requirement_path(data_requirement)

    def install(self):
        """Main method to install the dataset(s) by launching child process(es).

            Returns
            -------
                `list` [string] : list of path(s) to the installed data directory(ies)
        """
        print("---- repo2data starting ----")
        print(os.path.dirname(__file__))
        print("Config from file :")
        print(self._data_requirement_path)

        ret = []
        # Here we check if the first item is a dict (mutiple requirement)
        if isinstance(self._data_requirement_file[next(iter(self._data_requirement_file))], dict):
            for key, value in self._data_requirement_file.items():
                if isinstance(value, dict):
                    ret += [Repo2DataChild(value, self._use_server,
                                           self._data_requirement_path,key,self._server_dst_folder).install()]
        # if not, it is a single assignment
        else:
            ret += [Repo2DataChild(self._data_requirement_file,
                                   self._use_server, self._data_requirement_path, None, self._server_dst_folder).install()]

        return ret


class Repo2DataChild():
    """Repo2data child class which install the dataset"""

    def __init__(self, data_requirement_file=None, use_server=False, data_requirement_path=None, download_key = None, server_dst_folder=None):
        """Initialize the Repo2Data child class.
            Parameters
            ----------
                data_requirement_file : json
                    un-nested requirement in json format
                server : bool
                    whether to force output directory (default: False)
        """
        self._data_requirement_file = None
        self._dst_path = None
        self._use_server = use_server
        self._data_requirement_path = data_requirement_path
        self._server_dst_folder = server_dst_folder
        self._download_key = download_key
        if self._download_key:
            self._cache_record = f"{self._download_key}_repo2data_cache_record.json"
        else: 
            self._cache_record = f"repo2data_cache_record.json"

        self.load_data_requirement(data_requirement_file)

    def load_data_requirement(self, data_requirement_file):
        """Load the json data requirement file and set destination folder"""
        # here we should load just a json data
        try:
            input = json.dumps(data_requirement_file)
            json.loads(input)
            self._data_requirement_file = data_requirement_file
        except TypeError:
            print("Could not load json data.")
            raise

        if self._use_server:
            self._dst_path = os.path.join(
                self._server_dst_folder, self._data_requirement_file["projectName"])
        else:
            if ("dataLayout" in self._data_requirement_file.keys()) & (self._data_requirement_path is not None):
                if os.path.exists(self._data_requirement_path):
                    # data layout for neurolibre
                    if self._data_requirement_file['dataLayout'] == "neurolibre":
                        data_req_dir = os.path.dirname(
                            self._data_requirement_path)
                        self._dst_path = os.path.join(os.path.realpath(
                            os.path.join(data_req_dir, "..", "data")), self._data_requirement_file["projectName"])
            else:
                self._dst_path = os.path.join(
                    self._data_requirement_file["dst"], self._data_requirement_file["projectName"])

    def _archive_decompress(self):
        """Uncompress the archive with patoolib library"""
        files = os.listdir(self._dst_path)
        for file in files:
            try:
                patoolib.extract_archive(os.path.join(
                    self._dst_path, file), outdir=self._dst_path, interactive=False)
                # now we can safely delete the archive
                if os.path.exists(os.path.join(self._dst_path, file)):
                    os.remove(os.path.join(self._dst_path, file))
                print("Info : %s Decompressed" % (file))
            except patoolib.util.PatoolError:
                # we want to print the list of available formt JUST if the file is indeed an archive
                try:
                    patoolib.get_archive_format(
                        os.path.join(self._dst_path, file))
                    print("Info : %s is not compatible with patoolib "
                          ", bypassing decompression..." % (file))
                    list_formats = str(patoolib.list_formats())
                    print("Info: available archive formats :" + list_formats)
                except patoolib.util.PatoolError:
                    pass

    def _already_downloaded(self):
        """Check if data was already downloaded"""
        cache_rec_path = os.path.join(self._dst_path, self._cache_record)
        # The configuration file was saved if the data was correctly downloaded
        if not os.path.exists(cache_rec_path):
            is_downloaded = False
        else:
            # check content
            with open(cache_rec_path, 'r') as f:
                cache_rec = json.load(f)
            # If the cache record file is identical to 
            # the current data requirement file, assume that
            # the cached data exists.
            if self._data_requirement_file == cache_rec:
                is_downloaded = True
            else:
                is_downloaded = False
        return is_downloaded

    def _url_download(self):
        """
        Under the assumption that the download link points to 
        a single tar/zip etc file, use requests library to 
        downlad the data to a relative path.
        """
        url = self._data_requirement_file["src"]
        directory = self._dst_path
        max_retries = 3
        retry_delay = 5
        for retry in range(max_retries):
                response = requests.get(url, stream=True)
                if response.status_code == 200:
                    # Create the directory if it doesn't exist
                    if not os.path.exists(directory):
                        os.makedirs(directory)
                    # Get the filename from the URL
                    filename = url.split('/')[-1]
                    # Path to save the file
                    filepath = os.path.join(directory, filename)
                    # Save the content of the response to a file
                    with open(filepath, 'wb') as file:
                        for chunk in response.iter_content(chunk_size=128):
                            file.write(chunk)
                    print(f'File downloaded to: {filepath}')
                    return filepath
                else:
                    print(f'Attempt {retry + 1} - Failed to download the file. Status code: {response.status_code}')
                    if retry < max_retries - 1:
                        print(f'Retrying in {retry_delay} seconds...')
                        time.sleep(retry_delay)
        # If hits here means retries failed.
        print('Download failed after multiple attempts.')

    def _gdrive_download(self):
        """Install the data with google drive utility"""
        print("Info : Starting to download from Google drive %s ..." %
              (self._data_requirement_file["src"]))
        try:
            # gdown does not allow to give output dir
            cwd = os.getcwd()
            os.chdir(self._dst_path)
            subprocess.check_call(
                ['gdown', self._data_requirement_file["src"]])
            os.chdir(cwd)
        except FileNotFoundError:
            print("Error: gdown does not appear to be installed")
            raise

    def _datalad_download(self):
        """Install the data with datalad software"""
        print("Info : Starting to download from datalad %s ..." %
              (self._data_requirement_file["src"]))
        try:
            subprocess.check_call(
                ['datalad', 'install', self._dst_path, "-s", self._data_requirement_file["src"]])
        except FileNotFoundError:
            print("Error: datalad does not appear to be installed")
            raise

    def _lib_download(self):
        """Install the data with python library"""
        str_cmd = self._data_requirement_file["src"]
        str_cmd = str_cmd.replace("_dst", "\"" + self._dst_path + "\"")
        print("Info : Starting to download from python lib %s ..." %
              (self._data_requirement_file["src"]))
        subprocess.check_call(["python3", "-c", str_cmd])

    def _zenodo_download(self):
        """Install the data with zenodo_get utility"""
        print("Info : Starting to download from zenodo %s ..." %
              (self._data_requirement_file["src"]))
        try:
            subprocess.check_call(
                ['zenodo_get', '-o', self._dst_path, self._data_requirement_file["src"]])
        except FileNotFoundError:
            print("Error: zenodo_get does not appear to be installed")
            raise

    def _s3_download(self):
        """Install the data with amazon AWS s3 utility"""
        print("Info : Starting to download from s3 %s ..." %
              (self._data_requirement_file["src"]))
        try:
            subprocess.check_call(['aws', 's3', 'sync', '--no-sign-request',
                                  self._data_requirement_file["src"], self._dst_path])
        except FileNotFoundError:
            print("Error: aws does not appear to be installed")
            raise

    def _osf_download(self):
        """Install the data with OSF utility"""
        print("Info : Starting to download from osf {} ...".format(
            self._data_requirement_file["src"]))
        try:
            project_id = re.match(
                "https://osf.io/(.{5})", self._data_requirement_file["src"])[1]
            if not "remote_filepath" in self._data_requirement_file.keys():
                subprocess.check_call(
                    ['osf', '--project', project_id, 'clone', self._dst_path])
            else:
                remote_filepaths = self._data_requirement_file["remote_filepath"]
                if not isinstance(remote_filepaths, list):
                    remote_filepaths = [remote_filepaths]
                for remote_filepath in remote_filepaths:
                    subprocess.check_call(["osf", "--project", project_id, "fetch", "-f",
                                          remote_filepath, os.path.join(self._dst_path, remote_filepath)])
        except FileNotFoundError:
            print("Error: osf does not appear to be installed")
            raise

    def _scan_dl_type(self):
        """Detect which function to use for download"""
        # If an http link is provided or the url does not match one of the providers
        # (osf, google, datalad, git), then fall back to requests to download the file.
        if ((re.match(".*?(https://).*?", self._data_requirement_file["src"])
                or re.match(".*?(http://).*?", self._data_requirement_file["src"]))
                and not re.match(".*?\\.git$", self._data_requirement_file["src"])
                and not re.match(".*?(drive\\.google\\.com).*?", self._data_requirement_file["src"])
                and not re.match(".*?(https://osf\\.io).*?", self._data_requirement_file["src"])):
            self._url_download()
        # if the source link has a .git, we use datalad
        elif re.match(".*?\\.git$", self._data_requirement_file["src"]):
            self._datalad_download()
        # or coming from google drive
        elif re.match(".*?(drive\\.google\\.com).*?", self._data_requirement_file["src"]):
            self._gdrive_download()
        # or maybe it is a python script
        elif re.match(".*?(import.*?;).*?", self._data_requirement_file["src"]):
            self._lib_download()
        # or a s3 link ?
        elif re.match(".*?(s3://).*?", self._data_requirement_file["src"]):
            self._s3_download()
        # or from zenodo ?
        elif re.match(".*?(10\.\d{4}/zenodo).*?", self._data_requirement_file["src"]):
            self._zenodo_download()
        # or osf
        elif re.match(".*?(https://osf.io).*?", self._data_requirement_file["src"]):
            self._osf_download()

    def install(self):
        """Main method to install the dataset.

            Returns
            -------
                string : path to the installed data directory
        """
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

            # TODO: How to manage datalad update
            with open(os.path.join(self._dst_path, self._cache_record), 'w') as fst:
                json.dump(self._data_requirement_file, fst)
        else:
            print('Info : %s already downloaded' % (self._dst_path))

        return self._dst_path
