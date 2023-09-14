from setuptools import setup

setup(
    name='HistoricRedditHandler',
    version='1.0',
    py_modules=['HRH', 'CLIEntryPoint'],
    install_requires=[
        'Click',
        'psutil',
        'qbittorrent-api',
        'zstandard',
    ],
    entry_points='''
        [console_scripts]
        hrh=CLIEntryPoint:main
    '''
)