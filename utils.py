import os
import sys
from ftplib import FTP
from tqdm import tqdm

from constants import FTP_PATH, BASE_PATH, DATA_FOLDER


def get_filename_from_path(path):
    """
    :param path
    :return: file name without type
    """
    return ".".join(path.split('/')[-1].split('.')[:-1])


def mkdir_p(path):
    """
    create folder if not exist
    :param path
    """
    if not os.path.exists(path):
        os.makedirs(path)


class FTPDownloader:
    """
    Downloader class for displaying progress bar while downloading
    """

    def __call__(self, vcf_file=''):
        ftp = FTP(FTP_PATH)
        ftp.login()
        file_name = vcf_file.split('/')[-1]
        ftp.cwd(BASE_PATH)
        with open(f'{DATA_FOLDER}/{file_name}', 'wb') as out_file:
            total = ftp.size(file_name)
            with tqdm(total=total,
                      unit_scale=True,
                      desc=f"{file_name}",
                      miniters=1,
                      file=sys.stdout,
                      leave=True
                      ) as pbar:
                def call_back(data):
                    file_length = len(data)
                    pbar.update(file_length)
                    out_file.write(data)

                ftp.retrbinary('RETR {}'.format(file_name), call_back)
        ftp.quit()
