from setuptools import setup

APP = ['main.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'packages': ['controllers', 'models', 'services', 'views', 'utils'],
    #'iconfile': 'icon.icns',  # if you have an icon file
    'plist': {
        'CFBundleName': 'BabyTracker',
        'CFBundleDisplayName': 'Baby Tracker',
        'CFBundleVersion': '0.1.0',
        'CFBundleIdentifier': 'com.yourdomain.babytracker',
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)