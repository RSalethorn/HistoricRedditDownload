from setuptools import setup

setup(
    name='HistoricRedditHandler',
    version='1.0',
    py_modules=[
        'HRH', 
        'CLIEntryPoint', 
        'TorrentThread', 
        'ConfigHandler', 
        'CSVWriteThread',
        'FieldTypes',
        'FilterThread',
        'MemoryHandler',
        'ProgressReporting',
        'TorrentInfoStorage',
        'ZstandardThread',
        'ZtstandardHandler'
    ],
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