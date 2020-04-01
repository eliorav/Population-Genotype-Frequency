import os
from glob import glob
from tqdm import tqdm
import pandas as pd
from constants import SAMPLES_FOLDER, MERGED_VCF_FILE_NAME, IMAGE_SHARE_FOLDER_PATH, VCF_BY_POPULATION_PATH, \
    VCF_BY_POPULATION_FOLDER, FREQ_BY_POPULATION_PATH, FREQ_BY_POPULATION_FOLDER
from docker_runner import VCFToolsDockerRunner, Plink2DockerRunner
from utils import get_filename_from_path


def calculate_freq_by_population():
    if not os.path.exists(FREQ_BY_POPULATION_PATH):
        print("calculating freq by population")
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


def create_merged_vcf_files(snps):
    pass

def prepare_subset_vcf_files_by_population():
    if not os.path.exists(VCF_BY_POPULATION_PATH):
        print("preparing subset vcf by population")
        os.makedirs(VCF_BY_POPULATION_PATH)
        vcf_tools_runner = VCFToolsDockerRunner()
        samples = glob(f"{SAMPLES_FOLDER}/*.csv")

        with tqdm(total=len(samples)) as pbar:
            for sample in samples:
                sample = sample.replace('\\', '/')
                sample_name = get_filename_from_path(sample)
                sample_path = "/".join([IMAGE_SHARE_FOLDER_PATH] + sample.split('/')[1:])
                pbar.set_description(f"Processing {sample_name}")
                vcf_tools_runner(f"vcf-subset -c {sample_path} {IMAGE_SHARE_FOLDER_PATH}/{MERGED_VCF_FILE_NAME} | fill-an-ac > "
                                 f"{IMAGE_SHARE_FOLDER_PATH}/{VCF_BY_POPULATION_FOLDER}/{sample_name}.vcf")
                pbar.update(1)


def prepare_sample_data():
    """
    Extract samples data for each population to a file
    """
    if not os.path.exists(SAMPLES_FOLDER):
        os.makedirs(SAMPLES_FOLDER)
        all_samples_df = pd.read_csv('./integrated_call_samples.ALL.panel', sep="\t")
        populations = all_samples_df['pop'].unique()

        for pop in populations:
            pop_df = all_samples_df[all_samples_df['pop'] == pop]['sample']
            pop_df.to_csv(f'{SAMPLES_FOLDER}/{pop}.samples.csv', header=False, index=False, sep='\t')


def main():
    """
    Main script
    """
    prepare_sample_data()
    create_merged_vcf_files('')
    prepare_subset_vcf_files_by_population()
    calculate_freq_by_population()


if __name__ == "__main__":
    main()
