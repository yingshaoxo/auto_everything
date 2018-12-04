from setuptools import setup, find_packages
from os.path import dirname, join, abspath

file_path = join(abspath(dirname(__file__)), "README.md")
with open(file_path) as f:
    long_description = f.read()

setup(name='auto_everything',
        version='2.7',
        description='do automate things on Linux',
        long_description=long_description,
        long_description_content_type='text/markdown',
        classifiers=[
            'Operating System :: POSIX :: Linux',
            'Programming Language :: Python :: 3',
            'Topic :: System',
            'License :: OSI Approved :: MIT License'
            ],
        keywords='Linux system automation',
        url='http://github.com/yingshaoxo/auto_everything',
        author='yingshaoxo',
        license='MIT',
        packages=find_packages(),
        include_package_data=False,
        )
