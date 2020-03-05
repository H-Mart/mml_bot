import io
import sys
import zipfile

import requests

# todo this doesn't work on linux
# todo maybe download chromium too if possible
# todo use docker container?
if sys.platform == 'win32':
    driver_os = 'chromedriver_win32.zip'
    filename = 'chromedriver.exe'
elif sys.platform == 'linux':
    driver_os = 'chromedriver_linux64.zip'
    filename = 'chromedriver'
elif sys.platform == 'darwin':
    driver_os = 'chromedriver_mac64.zip'
    filename = 'chromedriver'
else:
    raise Exception('cannot determine system')


LATEST_RELEASE = 'https://chromedriver.storage.googleapis.com/LATEST_RELEASE'
DRIVER = 'https://chromedriver.storage.googleapis.com/{ver}/{os}'


def unzip_driver(driver_zip):
    print('Unzipping...', end='')
    path = zipfile.ZipFile(driver_zip).extract(filename)
    print('Done')
    print('Extracted driver to', path)
    return path


def download_driver():
    print('Getting latest release info...')
    release_num = requests.get(LATEST_RELEASE)
    release_num.raise_for_status()
    print('Lastest release:', release_num.text)
    print('Getting driver zipfile...', end='')
    driver = requests.get(DRIVER.format(ver=release_num.text, os=driver_os))
    driver.raise_for_status()
    print('Done')
    return io.BytesIO(driver.content)


def get_driver():
    # todo allow custom path
    return unzip_driver(download_driver())
