# Repo2Data
Repo2Data is a **python3** package that automatically fecth data from a remote server, and decomrpess it if needed. Future development will fetch automatically 
 from amazon s3, with datalad for version control or with specific lib dataset (tf.keras.datasets, nilearn.datasets.fetch etc...).
 
###### Input
 
A `data_requirement.json` configuration file explaining what should be read, where should you store the data, a project name (folder) and if you want to download in a recursive way.

```
{ "src": "https://github.com/SIMEXP/Repo2Data/archive/master.zip",
  "dst": "/DATA",
  "projectName": "repo2data_test",
  "recursive": true}
```

###### Output

The content of the http server inside a folder.

## Dependencies
  
* awscli  
* datalad
* patool
* wget

## Install

**Package not yet pushed on pip3**
`pip3 install repo2data`

## Usage

```
repo2data -r /path/to/data_requirement.json
```

if you have the `data_requirement.json` on the current folder, you can just use use `repo2data` without any option.
