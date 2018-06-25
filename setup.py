from setuptools import setup, find_packages
from os.path import dirname, join, abspath

setup(name='auto_everything',
        version='1.8',
        description='do automate things on Linux',
        long_description=open(join(abspath(dirname(__file__)), "README.md")).read(),
        long_description_content_type='markdown',
        classifiers=[
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 3',
            'Topic :: System',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
            ],
        keywords='Linux system automation',
        url='http://github.com/yingshaoxo/auto_everything',
        author='yingshaoxo',
        license='GPLv3',
        packages=find_packages(),
        include_package_data=False,
        )
