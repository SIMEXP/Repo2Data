[![CircleCI](https://circleci.com/gh/SIMEXP/Repo2Data.svg?style=svg)](https://circleci.com/gh/SIMEXP/Repo2Data)
# Repo2Data 2.0
Repo2Data is a **python3** package that automatically fecth data from a remote server, and decomrpess it if needed. Future development will fetch automatically 
 from [amazon s3](https://docs.aws.amazon.com/AmazonS3/latest/dev/Welcome.html), [datalad](https://www.datalad.org/) for version control or specific python lib dataset (`tf.keras.datasets`, `nilearn.datasets.fetch` etc...).
 
##### Input
 
A `data_requirement.json` configuration file explaining what should be read, where should you store the data, a project name (folder) and if you want to download in a recursive way.

```
{ "src": "https://github.com/SIMEXP/Repo2Data/archive/master.zip",
  "dst": "/DATA",
  "projectName": "repo2data_out",
  "recursive": true}
```

##### Output

The content of the server inside a folder.

##### Examples

###### archive file

Repo2Data will use wget if he detects a http link.
If the file is an archive, it will automatically decompress it using [patool](https://github.com/wummel/patool).

WARNING : Please unsure that you download the right package to unarchive the data (ex: `/usr/bin/pigz` for `.tar.gz` which should be installed by default on ubuntu).

```
{ "src": "https://github.com/SIMEXP/Repo2Data/archive/master.tar.gz",
  "dst": "/DATA",
  "projectName": "repo2data_out",
  "recursive": true}
```

###### library data-package

You need to put the script to donwload the data in the `src` field. You will need to install the lib on the host machine and import it in the script.

The function to fetch the data needs a parameter to provide the output directory, or Repo2Data can't control where the data will be stored. Please replace the parameter for the output dir by `_dst`, for example write :
`tf.keras.datasets.mnist.load_data(path=_dst)` instead of `tf.keras.datasets.mnist.load_data(path=/path/to/your/data)`
Repo2Data will then automatically replace `_dst` by the one provided in the `dst` field

```
{ "src": "import tensroflow as tf; tf.keras.datasets.mnist.load_data(path=_dst)",
  "dst": "/DATA",
  "projectName": "repo2data_out",
  "recursive": true}
```

###### datalad

If using datalad, it should be a `.git` file.

```
{ "src": "https://github.com/OpenNeuroDatasets/ds000005.git",
  "dst": "/DATA",
  "projectName": "repo2data_out",
  "recursive": true}
```

###### s3

To download an amazon s3 link, just put it on the `src` field.

```
{ "src": "s3://openneuro.org/ds000005",
  "dst": "/DATA",
  "projectName": "repo2data_out",
  "recursive": true}
```

###### multiple data

If you need to download many data at once, you can create a list of json. For example, to download different files from a repo :

```
{
  "authors": {
    "src": "https://github.com/tensorflow/tensorflow/blob/master/AUTHORS",
    "dst": "/DATA",
    "projectName": "repo2data_multiple1",
    "recursive": true
  },
  "license": {
    "src": "https://github.com/tensorflow/tensorflow/blob/master/LICENSE",
    "dst": "/DATA",
    "projectName": "repo2data_multiple2",
    "recursive": true
  }
}
```

###### disabling `dst` field

You can disable the field `dst` by using the option
`repo2data --server`

In this case Repo2Data will put the data from where it is run. This is usefull if you want to have full control over the destination (you are a server admin and don't want your users to control the destination).

## Dependencies
  
* awscli  
* datalad*
* patool
* wget
* pytest

(\*) To run Datalad, you will also need to install the latest version of [git-annex](https://git-annex.branchable.com/install/).
To install the latest version, please use the [package from neuro-debian](https://git-annex.branchable.com/install/) :
```
wget -O- http://neuro.debian.net/lists/stretch.us-nh.full | sudo tee /etc/apt/sources.list.d/neurodebian.sources.list
sudo apt-key adv --recv-keys --keyserver hkp://ipv4.pool.sks-keyservers.net:80 0xA5D32F012649A5A9
```
If you have troubles to download the key, please look at this [issue](https://github.com/jacobalberty/unifi-docker/issues/64).

## Install

###### With pip
`pip3 install repo2data`

## Usage

```
repo2data -r /path/to/data_requirement.json
```

if you have the `data_requirement.json` on the current folder, you can just use use `repo2data` without any option.
