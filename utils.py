import os
import requests
from tqdm import tqdm


def get_filename_from_path(path):
    """
    :param path
    :return: file name without type
    """
    return ".".join(path.replace('\\', '/').split('/')[-1].split('.')[:-1])


def mkdir_p(path):
    """
    create folder if not exist
    :param path
    """
    if not os.path.exists(path):
        os.makedirs(path)


def download_from_url(url, dst, desc=None):
    """
    :param url: to download file
    :param dst: place to put the file
    :param desc: the description of the download for the progress bar
    """
    file_size = int(requests.head(url, allow_redirects=True).headers["Content-Length"])
    if os.path.exists(dst):
        first_byte = os.path.getsize(dst)
    else:
        first_byte = 0
    if first_byte >= file_size:
        return
    if desc is None:
        desc = url.split('/')[-1]
    header = {"Range": "bytes=%s-%s" % (first_byte, file_size)}
    with tqdm(total=file_size, initial=first_byte, unit='B', unit_scale=True, desc=desc) as pbar:
        req = requests.get(url, headers=header, stream=True, allow_redirects=True)
        with(open(dst, 'ab')) as out_file:
            for chunk in req.iter_content(chunk_size=1024):
                if chunk:
                    out_file.write(chunk)
                    pbar.update(1024)
