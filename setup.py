from setuptools import setup, find_packages

setup(
    name='mypackage',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        Flask>=1.1.2,
        TTS>=0.8.0,
        runpod,
    ],
    entry_points={
        'console_scripts': [
            'mycommand = mypackage.module:main',
        ],
    },
)
