import os
from glob import glob
import pandas as pd
from tqdm import tqdm
from constants import SNPS_DATA_PATH, SNPS_DATA_FILE_NAME, FREQ_BY_POPULATION_PATH, DATA_FOLDER, \
    RESULT_FREQ_FILE_NAME, VCF_BY_POPULATION_PATH, IMAGE_SHARE_FOLDER_PATH, FREQ_BY_POPULATION_FOLDER
from services.docker_runner import Plink2DockerRunner
from utils import get_filename_from_path


def create_merged_freq_file():
    """
    create the final freq file by merging the freq by population and the SNPs data
    """
    print("create final freq file")
    res = pd.read_csv(f'{SNPS_DATA_PATH}/{SNPS_DATA_FILE_NAME}')
    freq_by_population_files = glob(f'{FREQ_BY_POPULATION_PATH}/*.afreq')

    for idx, pop_file in enumerate(freq_by_population_files):
        population = get_filename_from_path(pop_file).split('.')[0]
        pop_df = pd.read_csv(pop_file, sep="\t")
        if idx == 0:
            pop_df = pop_df.drop(columns=['#CHROM', 'OBS_CT']).rename(
                columns={"ID": "rsid", "REF": "A1 ", "ALT": "A2", "ALT_FREQS": population})
        else:
            pop_df = pop_df.drop(columns=['#CHROM', 'OBS_CT', 'REF', 'ALT']).rename(
                columns={"ID": "rsid", "ALT_FREQS": population})
        res = pd.merge(res, pop_df, on='rsid')
    res.to_csv(f'{DATA_FOLDER}/{RESULT_FREQ_FILE_NAME}', sep="\t", index=False)


def calculate_freq_by_population():
    """
    calculate freq by population
    """
    if not os.path.exists(FREQ_BY_POPULATION_PATH):
        print("calculating freq by population. it can take a while")
        os.makedirs(FREQ_BY_POPULATION_PATH)
        plink_runner = Plink2DockerRunner()
        samples = glob(f"{VCF_BY_POPULATION_PATH}/*.vcf")

        with tqdm(total=len(samples)) as pbar:
            for vcf_sample in samples:
                vcf_sample = vcf_sample.replace('\\', '/')
                vcf_file_name = get_filename_from_path(vcf_sample)
                sample_path = "/".join([IMAGE_SHARE_FOLDER_PATH] + vcf_sample.split('/')[1:])
                pbar.set_description(f"Processing {vcf_file_name}")
                plink_runner(f"./plink2 --vcf {sample_path} --freq "
                             f"--out {IMAGE_SHARE_FOLDER_PATH}/{FREQ_BY_POPULATION_FOLDER}/{vcf_file_name}")
                pbar.update(1)
    else:
        print(f"freq by population already exists in {FREQ_BY_POPULATION_PATH}")


def prepare_freq_data():
    """
    prepare freq data
    """
    calculate_freq_by_population()
    create_merged_freq_file()
