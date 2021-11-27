# author: Group 24
# date: 2021-11-19

'''This script downloads data from the given url to a local path and perform unzip if needed.

Usage: download_data.py --url=<url> --file_path=<file_path> [--zip_file_name=<zip_file_name>]

Options:
--url=<url>   Path of the data set to be downloaded
--file_path=<file_path>   Path(includes filename if not zip) to the data file store in local
--zip_file_name=<zip_file_name> File name inside the zip file that wants to unzip, in case the source is a zip file (Optional option)
'''
from urllib.request import urlopen
from zipfile import ZipFile
from io import BytesIO
import os
import pandas as pd
from docopt import docopt

opt = docopt(__doc__)


def download_and_unzip(url, file_path, zip_file_name):
    """download data from the url. If the file is zipped, also unzip the target file.

    Parameters
    ----------
    url : string
        url of the file to be downloaded
    file_path : string
        local path to save the file
    zip_file_name : string
        file name that needs to be extracted from the zip

    Examples
    --------
    >>> download_and_unzip(url, file_path, zip_file_name)
    """

    try:
        response = urlopen(url)
        zipfile = ZipFile(BytesIO(response.read()))
        zipfile.extract(member=zip_file_name, path=file_path)
        print(f"The file is unzipped successfully at %s/%s" %
              (file_path, zip_file_name))
    except Exception as error:
        print(f"Error message: %s" % error)
        print("Please check if the url points to a zip file!")
    return


def main(url, file_path, zip_file_name=None):

    if zip_file_name is not None:
        download_and_unzip(url, file_path, zip_file_name)
    else:
        data = pd.read_csv(url, header=None)

        if not os.path.exists(file_path):
            os.makedirs(os.path.dirname(file_path))

        data.to_csv(file_path, index=False)
        print(f"The file is downloaded successfully at %s" % file_path)


if __name__ == "__main__":
    main(opt['--url'], opt['--file_path'], opt['--zip_file_name'])
