from setuptools import setup

setup(name='repo2data',
      version='',
      description='Automatic data fetcher from a remote server.',
      url='https://github.com/SIMEXP/Repo2Data',
      download_url='https://github.com/SIMEXP/Repo2Data/archive/.tar.gz',
      author='Loic TETREL',
      author_email='loic.tetrel.pro@gmail.com',
      license='MIT',
      packages=['repo2data'],
      scripts=['bin/repo2data'],
      install_requires=[
          'awscli',
          'patool',
      #seg-fault with datalad
          'datalad',
          'wget',
          'osfclient',
          'gdown',
      ],
      include_package_data=True,
      zip_safe=False)
