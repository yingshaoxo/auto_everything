from setuptools import setup, find_packages

setup(name='auto_everything',
        version='0.4',
        description='do automate thing on Linux',
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


