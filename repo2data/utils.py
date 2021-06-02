import os
import codecs

def read(relative_path):
    """Read the curent file.
    Parameters
    ----------
        relative_path : string, required
            relative path to the file to be read, from the directory of this file
    
    Returns
    -------
        string : content of the file at relative path
    """
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, relative_path), 'r') as fp:
        return fp.read()

def get_version():
    """Get the version of this software, as describe in the __init__.py file from the top module.
    
    Returns
    -------
        string : version of this software
    """
    os.path.dirname(__file__)
    relative_path = "__init__.py"
    for line in read(relative_path).splitlines():
        if line.startswith('__version__'):
            delim = '"' if '"' in line else "'"
            return line.split(delim)[1]
    else:
        raise RuntimeError("Unable to find version string.")