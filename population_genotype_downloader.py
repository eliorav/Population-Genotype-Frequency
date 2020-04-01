import os
import sys
from ftplib import FTP
from multiprocessing import Pool
from tqdm import tqdm

FTP_PATH = 'ftp.1000genomes.ebi.ac.uk'
BASE_PATH = '/vol1/ftp/release/20130502/'
DATA_FOLDER = '.data'
SAMPLES_FOLDER = 'samples'

PSAM_PATH = 'https://www.dropbox.com/s/yozrzsdrwqej63q/phase3_corrected.psam?dl=1'
PVAR_PATH = 'https://www.dropbox.com/s/op9osq6luy3pjg8/all_phase3.pvar.zst?dl=1'
PGEN_PATH = 'https://www.dropbox.com/s/afvvf1e15gqzsqo/all_phase3.pgen.zst?dl=1'


class Downloader:
    """
    Downloader class for displaying progress bar while downloading
    """
    def __call__(self, data):
        idx, sample = data
        ftp = FTP(FTP_PATH)
        ftp.login()
        file_name = sample.split('/')[-1]
        ftp.cwd(BASE_PATH)
        with open(f'{DATA_FOLDER}/{file_name}', 'wb') as out_file:
            total = ftp.size(file_name)
            with tqdm(total=total,
                      unit_scale=True,
                      desc=f"{idx} - {file_name}",
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


def download_genotype_data(pool_size=1):
    """
    Download genotype data the save the out put in .data dir
    :param pool_size: the size of parallels downloads
    """
    if not os.path.exists(DATA_FOLDER):
        os.makedirs(DATA_FOLDER)
    downloader = Downloader()
    ftp = FTP(FTP_PATH)
    ftp.login()
    ftp.cwd(BASE_PATH)
    population_files = [data for data in ftp.nlst() if 'ALL' in data and 'chr' in data]

    with Pool(pool_size) as pool:
        pool.map(downloader, enumerate(population_files))


download_genotype_data()


'''
TOOD:
1. download pgen, psam, pvar from http://www.cog-genomics.org/plink/2.0/resources#1kg_phase3 - boldfaced links
2. -zst-decompress the pgen and the pvar files using plink2
3. ./plink2 --pfile ./share_folder/all_phase3 vzs --extract ./share_folder/rsid_list.tsv --export vcf --out ./share_folder/all_phase3 - conver to vcf
4. ./plink2 --vcf ./share_folder/all_phase3.vcf --freq --out ./share_folder/all_phase3.freq  - get freq data
4. ./plink2 --vcf ./share_folder/ALL.chr1.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf --freq --out ./share_folder/ALL.chr1.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes  - get freq data
5. cleanup


grep CEU ./share_folder/integrated_call_samples_v3.20130502.ALL.panel | cut -f1 > ./share_folder/CEU.samples.list
docker run --rm -it -v "//e/work/Population-Genotype-Frequency/.data://usr/src/app/share_folder" avelior/vcftools bash -c "vcf-subset -c ./share_folder/CEU.samples.list ./share_folder/ALL.chr1.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf"

vcf-subset -c ./share_folder/CEU.samples.list ./share_folder/ALL.chr1.phase3_shapeit2_mvncall_integrated_v5a.20130502.genotypes.vcf
'''

def download_merged_dataset_files():
    """
    TODO
    """
    pass

def decompress_file(file_name):
    """
    TODO
    """
    pass

def create_vcf():
    """
    TODO
    """
    pass

def get_freq_data():
    """
    TODO
    """
    pass

