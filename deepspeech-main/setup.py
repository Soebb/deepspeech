#! /usr/bin/env python

from setuptools import setup, Extension
from distutils.command.build import build

import os
import subprocess
import sys

class get_numpy_include(object):
    """Defer numpy.get_include() until after numpy is installed."""

    def __str__(self):
        import numpy
        return numpy.get_include()

def main():

    def read(fname):
        return open(os.path.join(os.path.dirname(__file__), fname)).read()


    class BuildExtFirst(build):
        sub_commands = [('build_ext', build.has_ext_modules),
                        ('build_py', build.has_pure_modules),
                        ('build_clib', build.has_c_libraries),
                        ('build_scripts', build.has_scripts)]

    # Properly pass arguments for linking, setuptools will perform some checks
    def lib_dirs_split(a):
        if os.name == 'posix':
            return a.split('-L')[1:]

        if os.name == 'nt':
            return []

        raise AssertionError('os.name == java not expected')

    def libs_split(a):
        if os.name == 'posix':
            return a.split('-l')[1:]

        if os.name == 'nt':
            return a.split('.lib')[0:1]

        raise AssertionError('os.name == java not expected')

    ds_ext = Extension(name='deepspeech._impl',
                       sources=['impl.i'],
                       include_dirs=[get_numpy_include(), '../'],
                       library_dirs=list(map(lambda x: x.strip(), lib_dirs_split(os.getenv('MODEL_LDFLAGS', '')))),
                       libraries=list(map(lambda x: x.strip(), libs_split(os.getenv('MODEL_LIBS', '')))),
                       swig_opts=['-c++', '-keyword'])

    project_version='0.9.3'
    setup(name='deepspeech',
          description='A library for running inference on a DeepSpeech model',
          long_description=read('README.rst'),
          long_description_content_type='text/x-rst; charset=UTF-8',
          author='Mozilla',
          version=project_version,
          package_dir={'deepspeech': '.'},
          cmdclass={'build': BuildExtFirst},
          license='MPL-2.0',
          url='https://github.com/mozilla/DeepSpeech',
          project_urls={
              'Documentation': 'https://github.com/mozilla/DeepSpeech/tree/v{}#project-deepspeech'.format(project_version),
              'Tracker': 'https://github.com/mozilla/DeepSpeech/issues',
              'Repository': 'https://github.com/mozilla/DeepSpeech/tree/v{}'.format(project_version),
              'Discussions': 'https://discourse.mozilla.org/c/deep-speech',
          },
          ext_modules=[ds_ext],
          py_modules=['deepspeech', 'deepspeech.client', 'deepspeech.impl'],
          entry_points={'console_scripts':['deepspeech=deepspeech.client:main']},
          install_requires=['numpy==1.19.5'],
          include_package_data=True,
          classifiers=[
              'Development Status :: 3 - Alpha',
              'Environment :: Console',
              'Intended Audience :: Developers',
              'Intended Audience :: Science/Research',
              'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
              'Programming Language :: Python :: 2.7',
              'Programming Language :: Python :: 3.4',
              'Programming Language :: Python :: 3.5',
              'Programming Language :: Python :: 3.6',
              'Topic :: Multimedia :: Sound/Audio :: Speech',
              'Topic :: Scientific/Engineering :: Human Machine Interfaces',
              'Topic :: Scientific/Engineering',
              'Topic :: Utilities',
          ])

if __name__ == '__main__':
    main()
