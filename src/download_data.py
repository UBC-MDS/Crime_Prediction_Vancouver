# author: Group 24
# date: 2021-11-19

'''This script downloads data from the given url to a local path and perform unzip if needed.

Usage: download_data.py --url=<url> --file_path=<file_path> [--zip_file_name=<zip_file_name>]

Options:
--url=<url>   Path of the data set to be downloaded
--file_path=<file_path>   Path(includes filename if not zip) to the data file store in local
--zip_file_name=<zip_file_name> File name in case the source is a zip file (Optional option)
'''
from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO
import os
import pandas as pd
from docopt import docopt

opt = docopt(__doc__)

def download_and_unzip(url, file_path, zip_file_name):
    try:
        response = urlopen(url)
        zipfile = ZipFile(BytesIO(response.read()))
        zipfile.extract(member=zip_file_name, path=file_path)
    except Exception as error:
        print(f"Error message: %s" %error)        
        print("Please check if the url points to a zip file!")
    return

def main(url, file_path, zip_file_name=None):
    
    if zip_file_name is not None:
        download_and_unzip(url, file_path, zip_file_name)
    else:
        data = pd.read_csv(url, header=None)
        try:
          data.to_csv(file_path, index=False)
        except:
            os.makedirs(os.path.dirname(file_path))
            data.to_csv(file_path, index=False)

if __name__ == "__main__":
    main(opt['--url'], opt['--file_path'], opt['--zip_file_name'])
