[![CircleCI](https://circleci.com/gh/SIMEXP/Repo2Data.svg?style=svg)](https://circleci.com/gh/SIMEXP/Repo2Data) ![](https://img.shields.io/pypi/v/repo2data?style=flat&logo=python&logoColor=white&logoSize=8&labelColor=rgb(255%2C0%2C0)&color=white) [![Python 3.6](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/) ![GitHub](https://img.shields.io/github/license/SIMEXP/repo2data)
# Repo2Data
Repo2Data is a **python3** package that automatically fetches data from a remote server, and decompresses it if needed. Supported web data sources are [amazon s3](https://docs.aws.amazon.com/AmazonS3/latest/dev/Welcome.html), [datalad](https://www.datalad.org/), [osf](https://osf.io/), [Google drive](https://www.google.com/intl/en_ca/drive/), raw http(s) or specific python lib datasets (`sklearn.datasets.load`, `nilearn.datasets.fetch` etc...).
 
## Input
 
A `data_requirement.json` configuration file explaining what should be read, where should you store the data, and a project name (name of the folder where file will be downloaded).

```
{ "src": "https://github.com/SIMEXP/Repo2Data/archive/master.zip",
  "dst": "./data",
  "projectName": "repo2data_out"}
```
`src` is where you configure the upstream location for your data.

`dst` specifies where (which folder) the data should be downloaded.

`projectName` is the name of the directory where the data will be saved, such that you can access it at `{dst}/{projectName}`

## Output

The content of the server inside the specified folder.

## Execution

The tool can be executed through `bash` or imported as a python API.

#### Bash

If `data_requirement.json` is inside current directory, you can call the following on the command line:

```
repo2data
```

#### Python API

After defining the `data_requirement.json` and importing the module, first instanciate the `Repo2Data` object with:

```
from repo2data.repo2data import Repo2Data

# define data requirement path
data_req_path = os.path.join("data_requirement.json")
# download data
repo2data = Repo2Data(data_req_path)
```

You can then fetch the data with the `install` method, which returns a list to the output directory(ies) where the data was downloaded:
```
data_path = repo2data.install()
```

## Examples of data_requirement.json

###### archive file

Repo2Data will use `wget` if it detects a http link.
If this file is an archive, it will be automatically be decompressed using [patool](https://github.com/wummel/patool). Please unsure that you download the right package to unarchive the data (ex: `/usr/bin/tar` for `.tar.gz`).

```
{ "src": "https://github.com/SIMEXP/Repo2Data/archive/master.tar.gz",
  "dst": "./data",
  "projectName": "repo2data_wget"}
```

###### Google Drive

It can also download a file from [Google Drive](https://www.google.com/intl/en_ca/drive/) using [gdown](https://github.com/wkentaro/gdown).
You will need to make sure that your file is available **publically**, and get the project ID (a chain of 33 characters that you can find on the url).
Then you can construct the url with this ID:
`https://drive.google.com/uc?id=${PROJECT_ID}`

For example:
```
{ "src": "https://drive.google.com/uc?id=1_zeJqQP8umrTk-evSAt3wCLxAkTKo0lC",
  "dst": "./data",
  "projectName": "repo2data_gdrive"}
```

###### library data-package

You will need to put the script to import and download the data in the `src` field, the lib should be installed on the host machine.

Any lib function to fetch data needs a parameter so it know where is the output directory. To avoid dupplication of the destination parameter, please replace the parameter for the output dir in the function by `_dst`.

For example write `tf.keras.datasets.mnist.load_data(path=_dst)` instead of `tf.keras.datasets.mnist.load_data(path=/path/to/your/data)`.
Repo2Data will then automatically replace `_dst` by the one provided in the `dst` field.

```
{ "src": "import tensroflow as tf; tf.keras.datasets.mnist.load_data(path=_dst)",
  "dst": "./data",
  "projectName": "repo2data_lib"}
```

###### datalad

The `src` should be point to a `.git` link if using `datalad`, `Repo2Data` will then just call `datalad get`.

```
{ "src": "https://github.com/OpenNeuroDatasets/ds000005.git",
  "dst": "./data",
  "projectName": "repo2data_datalad"}
```

###### s3

To download an amazon s3 link, `Repo2Data` uses `aws s3 sync --no-sign-request` command. So you should provide the `s3://` bucket link of the data:

```
{ "src": "s3://openneuro.org/ds000005",
  "dst": "./data",
  "projectName": "repo2data_s3"}
```

###### osf

`Repo2Data` uses [osfclient](https://github.com/osfclient/osfclient) `osf -p PROJECT_ID clone` command. You will need to give the link to the **public** project containing your data `https://osf.io/.../`:

```
{ "src": "https://osf.io/fuqsk/",
  "dst": "./data",
  "projectName": "repo2data_osf"}
```

If you need to download a single file, or a list of files, you can do this using the `remote_filepath` field wich runs `osf -p PROJECT_ID fetch -f file`. For example to download two files (https://osf.io/aevrb/ and https://osf.io/bvuh6/), use a relative path to the root of the project:

```
{ "src": "https://osf.io/fuqsk/",
  "remote_filepath": ["hello.txt", "test-subfolder/hello-from-subfolder.txt"],
  "dst": "./data",
  "projectName": "repo2data_osf_multiple"}
```

###### zenodo

The public data repository [zenodo](https://zenodo.org/) is also supported using [zenodo_get](https://gitlab.com/dvolgyes/zenodo_get). Make sure your project is public and it has a DOI with the form `10.5281/zenodo.XXXXXXX`:

```
{ "src": "10.5281/zenodo.6482995",
  "dst": "./data",
  "projectName": "repo2data_zenodo"}
```

###### multiple data

If you need to download many data at once, you can create a list of json. For example, to download different files from a repo :

```
{
  "authors": {
    "src": "https://github.com/tensorflow/tensorflow/blob/master/AUTHORS",
    "dst": "./data",
    "projectName": "repo2data_multiple1"
  },
  "license": {
    "src": "https://github.com/tensorflow/tensorflow/blob/master/LICENSE",
    "dst": "./data",
    "projectName": "repo2data_multiple2"
  }
}
```
## Install

### Docker (recommended)

This is the recommended way of using `Repo2Data`, because it encapsulate all the dependencies inside the container. It also features `scikit-learn` and `nilearn` to pull data from.

Clone this repo and build the docker image yourself :
```
git clone https://github.com/SIMEXP/Repo2Data
sudo docker build --tag repo2data ./Repo2Data/
```

### pip

To install `Datalad` you will need the latest version of [git-annex](https://git-annex.branchable.com/install/), please use the [package from neuro-debian](https://git-annex.branchable.com/install/) :
```
wget -O- http://neuro.debian.net/lists/stretch.us-nh.full | sudo tee /etc/apt/sources.list.d/neurodebian.sources.list
sudo apt-key adv --recv-keys --keyserver hkp://ipv4.pool.sks-keyservers.net:80 0xA5D32F012649A5A9
```
If you have troubles to download the key, please look at this [issue](https://github.com/jacobalberty/unifi-docker/issues/64).

You can now install with `pip`:
```
python3 -m pip install repo2data
```

## Usage

After creating the `data_requirement.json`, just use `repo2data` without any option:
```
repo2data
```

### requirement in another directory

If the `data_requirement.json` is in another directory, use the `-r` option:
```
repo2data -r /PATH/TO/data_requirement.json
```

### github repo url as input

Given a valid https github repository with a `data_requirement.json` at `HEAD` branch (under a `binder` directory or at its root), you can do:
```
repo2data -r GITHUB_REPO
```

An example of a valid `GITHUB_REPO` is: https://github.com/ltetrel/repo2data-caching-s3

### Trigger re-fetch

When you re-run Repo2Data with the same destination, it will automatically look for an existing `data_requirement.json` file in the downloaded folder.
If the configured `data_requirement.json` is the same (i.e. the [JSON dict](https://www.w3schools.com/python/python_json.asp) has the same fields) then it will not re-download.

To force the re-fetch (update existing files, add new files but keep the old files), you can add a new field or update an existing one in the `data_requirement.json`.
For example replace:
```
{ "src": "https://github.com/SIMEXP/Repo2Data/archive/master.zip",
  "dst": "./data",
  "projectName": "repo2data_out"}
```
by 
```
{ "src": "https://github.com/SIMEXP/Repo2Data/archive/master.zip",
  "dst": "./data",
  "projectName": "repo2data_out",
  "version": "1.1"}
```
This is especially usefull when the provenance link always stay the same (osf, google drive...).

### make `dst` field optionnal

##### using `dataLayout` field
In the case you have a fixed known layout for the data folder within a github repository, the `dst` field is not needed anymore.
To define what kind of layout you want, you can use the `dataLayout` field.
For now we just support the [neurolibre layout](https://docs.neurolibre.org/en/latest/SUBMISSION_STRUCTURE.html#preprint-repository-structure):
```
{ "src": "https://github.com/SIMEXP/Repo2Data/archive/master.zip",
  "dataLayout": "neurolibre"}
```
If you need another data layout (like [YODA](https://f1000research.com/posters/7-1965) or [cookiecutter-data-science](https://drivendata.github.io/cookiecutter-data-science/)) you can create a feature request.

##### for administrator
You can disable the field `dst` by using the option
`repo2data --server`

In this case `Repo2Data` will put the data inside the folder `./data` from where it is run. This is usefull if you want to have full control over the destination (you are a server admin and don't want your users to control the destination).

### Docker

You will need to create a folder on your machine (containing a `data_requirement.json`) that the Docker container will access so `Repo2Data` can pull the data inside it, after you can use:
```
sudo docker run -v /PATH/TO/FOLDER:/data repo2data
```

(the container will run with `--server` enabled, so all the data in the container will be at `/data`)

A requirement from a github repo is also supported (so you don't need any `data_requirement.json` inside your host folder):
```
sudo docker run -v /PATH/TO/FOLDER:/data repo2data -r GITHUB_REPO
```

`Docker` mounts the host (your machine) folder into the container folder as `-v host_folder:container_folder`, so don't override `:/data`.

