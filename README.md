[![CircleCI](https://circleci.com/gh/SIMEXP/Repo2Data.svg?style=svg)](https://circleci.com/gh/SIMEXP/Repo2Data) [![PyPI version](https://badge.fury.io/py/repo2data.svg)](https://badge.fury.io/py/repo2data) [![Python 3.6](https://img.shields.io/badge/python-3.6+-blue.svg)](https://www.python.org/downloads/release/python-360/) ![GitHub](https://img.shields.io/github/license/SIMEXP/repo2data)
# Repo2Data
Repo2Data is a **python3** package that automatically fecth data from a remote server, and decompress it if needed. Supported web data sources are [amazon s3](https://docs.aws.amazon.com/AmazonS3/latest/dev/Welcome.html), [datalad](https://www.datalad.org/), [osf](https://osf.io/), raw http(s) or specific python lib datasets (`sklearn.datasets.load`, `nilearn.datasets.fetch` etc...).
 
## Input
 
A `data_requirement.json` configuration file explaining what should be read, where should you store the data, a folder name and if you want to download in a recursive way.

```
{ "src": "https://github.com/SIMEXP/Repo2Data/archive/master.zip",
  "dst": "./data",
  "projectName": "repo2data_out",
  "recursive": true}
```
## Output

The content of the server inside the specified folder.

### Examples of data_requirement.json

###### archive file

Repo2Data will use `wget` if it detects a http link.
If this file is an archive, it will be automatically be decompressed using [patool](https://github.com/wummel/patool). Please unsure that you download the right package to unarchive the data (ex: `/usr/bin/tar` for `.tar.gz`).

```
{ "src": "https://github.com/SIMEXP/Repo2Data/archive/master.tar.gz",
  "dst": "./data",
  "projectName": "repo2data_wget",
  "recursive": true}
```

###### library data-package

You will need to put the script to import and download the data in the `src` field, the lib should be installed on the host machine.

Any lib function to fetch data needs a parameter so it know where is the output directory. To avoid dupplication of the destination parameter, please replace the parameter for the output dir in the function by `_dst`.

For example write `tf.keras.datasets.mnist.load_data(path=_dst)` instead of `tf.keras.datasets.mnist.load_data(path=/path/to/your/data)`.
Repo2Data will then automatically replace `_dst` by the one provided in the `dst` field.

```
{ "src": "import tensroflow as tf; tf.keras.datasets.mnist.load_data(path=_dst)",
  "dst": "./data",
  "projectName": "repo2data_lib",
  "recursive": true}
```

###### datalad

The `src` should be point to a `.git` link if using `datalad`, `Repo2Data` will then just call `datalad get`.

```
{ "src": "https://github.com/OpenNeuroDatasets/ds000005.git",
  "dst": "./data",
  "projectName": "repo2data_datalad",
  "recursive": true}
```

###### s3

To download an amazon s3 link, `Repo2Data` uses `aws s3 sync --no-sign-request` command. So you should provide the `s3://` bucket link of the data:

```
{ "src": "s3://openneuro.org/ds000005",
  "dst": "./data",
  "projectName": "repo2data_s3",
  "recursive": true}
```

###### osf

`Repo2Data` uses [osclient](https://github.com/osfclient/osfclient) `osf -p PROJECT_ID clone` command. You will need to give the link to your project containing your data `https://osf.io/.../`:

```
{ "src": "https://osf.io/fuqsk/",
  "dst": "./data",
  "projectName": "repo2data_osf",
  "recursive": true}
```

###### multiple data

If you need to download many data at once, you can create a list of json. For example, to download different files from a repo :

```
{
  "authors": {
    "src": "https://github.com/tensorflow/tensorflow/blob/master/AUTHORS",
    "dst": "./data",
    "projectName": "repo2data_multiple1",
    "recursive": true
  },
  "license": {
    "src": "https://github.com/tensorflow/tensorflow/blob/master/LICENSE",
    "dst": "./data",
    "projectName": "repo2data_multiple2",
    "recursive": true
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

## Dependencies
  
* awscli==1.16.163
* patool==1.12
* datalad==0.12.4 (see pip install section)
* wget==3.2
* pytest==4.4.0

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

### disabling `dst` field

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

