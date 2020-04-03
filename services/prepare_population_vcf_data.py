import os
from glob import glob
from time import sleep

from tqdm import tqdm

from constants import VCF_BY_POPULATION_PATH, SAMPLES_FOLDER, IMAGE_SHARE_FOLDER_PATH, MERGED_VCF_FILE_NAME, \
    VCF_BY_POPULATION_FOLDER, GENOTYPE_DATA_FOLDER
from services.docker_runner import VCFToolsDockerRunner
from utils import get_filename_from_path


def prepare_subset_vcf_files_by_population():
    """
    Split the merged VCF file into multiple VCF files by population
    """
    if not os.path.exists(VCF_BY_POPULATION_PATH):
        print("preparing subset vcf by population")
        os.makedirs(VCF_BY_POPULATION_PATH)
        sleep(10)
        vcf_tools_runner = VCFToolsDockerRunner()
        samples = glob(f"{SAMPLES_FOLDER}/*.csv")

        with tqdm(total=len(samples)) as pbar:
            for sample in samples:
                sample = sample.replace('\\', '/')
                sample_name = get_filename_from_path(sample)
                sample_path = "/".join([IMAGE_SHARE_FOLDER_PATH] + sample.split('/')[1:])
                pbar.set_description(f"Processing {sample_name}")
                vcf_tools_runner(
                    f"vcf-subset -c {sample_path} "
                    f"{IMAGE_SHARE_FOLDER_PATH}/{GENOTYPE_DATA_FOLDER}/{MERGED_VCF_FILE_NAME} | fill-an-ac > "
                    f"{IMAGE_SHARE_FOLDER_PATH}/{VCF_BY_POPULATION_FOLDER}/{sample_name}.vcf")
                pbar.update(1)
    else:
        print(f"Subset VCF files by population already exist in: {VCF_BY_POPULATION_PATH}")
