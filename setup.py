from setuptools import setup
import repo2data.utils

setup(name='repo2data',
      version=repo2data.utils.get_version(),
      description='To download data from a variety of providers.',
      url='https://github.com/SIMEXP/Repo2Data',
      download_url='https://github.com/SIMEXP/Repo2Data/archive/v{}.tar.gz'.format(repo2data.utils.get_version()),
      author='Loic TETREL',
      author_email='roboneurolibre@gmail.com',
      license='MIT',
      packages=['repo2data'],
      scripts=['bin/repo2data'],
      install_requires=[
          'awscli',
          'patool',
      #seg-fault with datalad
          'datalad',
          'requests',
          'osfclient',
          'gdown',
          'zenodo-get'
      ],
      include_package_data=True,
      zip_safe=False)
