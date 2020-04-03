import os
import shutil

from constants import GENOTYPE_DATA_PATH, PSAM_PATH, MERGED_GENOTYPE_FILE, PVAR_PATH, PGEN_PATH, \
    IMAGE_SHARE_FOLDER_PATH, GENOTYPE_DATA_FOLDER, SNP_LIST_FILE_NAME
from services.docker_runner import Plink2DockerRunner
from utils import download_from_url


def decompress_genotype_file(file_name):
    """
    decompress genotype file
    :param file_name
    """
    print(f"decompressing {file_name}")
    plink_runner = Plink2DockerRunner()
    file_path = f"{IMAGE_SHARE_FOLDER_PATH}/{GENOTYPE_DATA_FOLDER}/{file_name}"
    plink_runner(f"./plink2 --zst-decompress {file_path}.zst > {file_path}")


def download_genotype_data():
    """
    Download genotype data the save the out put in .data dir
    """
    print("downloading genotype data")
    download_from_url(PSAM_PATH, dst=f"{GENOTYPE_DATA_PATH}/{MERGED_GENOTYPE_FILE}.psam", desc="downloading psam")
    download_from_url(PVAR_PATH, dst=f"{GENOTYPE_DATA_PATH}/{MERGED_GENOTYPE_FILE}.pvar.zst",
                      desc="downloading pvar")
    download_from_url(PGEN_PATH, dst=f"{GENOTYPE_DATA_PATH}/{MERGED_GENOTYPE_FILE}.pgen.zst",
                      desc="downloading pgen")
    decompress_genotype_file(f"{MERGED_GENOTYPE_FILE}.pvar")
    decompress_genotype_file(f"{MERGED_GENOTYPE_FILE}.pgen")


def create_merged_genotype_file(snps_file_path):
    """
    create merged genotype file from psam pvar and pgen
    :param snps_file_path: the path of the SNPs list
    """
    print("creating merged genotype file")
    plink_runner = Plink2DockerRunner()
    shutil.copyfile(snps_file_path, f"{GENOTYPE_DATA_PATH}/{SNP_LIST_FILE_NAME}")
    plink_runner(f"./plink2 --pfile {IMAGE_SHARE_FOLDER_PATH}/{GENOTYPE_DATA_FOLDER}/{MERGED_GENOTYPE_FILE} vzs "
                 f"--extract {IMAGE_SHARE_FOLDER_PATH}/{GENOTYPE_DATA_FOLDER}/{SNP_LIST_FILE_NAME} --export vcf "
                 f"--out {IMAGE_SHARE_FOLDER_PATH}/{GENOTYPE_DATA_FOLDER}/{MERGED_GENOTYPE_FILE}")


def prepare_genotype_data(args):
    """
    Prepare genotype data
    :param args: script args - should include snps_file_path - the path of the SNPs list
    """
    if not os.path.exists(GENOTYPE_DATA_PATH):
        os.makedirs(GENOTYPE_DATA_PATH)
        download_genotype_data()
        create_merged_genotype_file(args.snps_file_path)
