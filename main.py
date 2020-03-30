import os
from glob import glob
from tqdm import tqdm
import pandas as pd
from constants import SAMPLES_FOLDER, MERGED_VCF_FILE_NAME, IMAGE_SHARE_FOLDER_PATH, VCF_BY_POPULATION_PATH, \
    VCF_BY_POPULATION_FOLDER
from docker_runner import VCFToolsDockerRunner


def prepare_subset_vcf_files():
    if not os.path.exists(VCF_BY_POPULATION_PATH):
        os.makedirs(VCF_BY_POPULATION_PATH)
        vcf_tools_runner = VCFToolsDockerRunner()
        samples = glob(f"{SAMPLES_FOLDER}/*.csv")

        with tqdm(total=len(samples)) as pbar:
            for sample in samples:
                sample = sample.replace('\\', '/')
                sample_name = ".".join(sample.split('/')[-1].split('.')[:-1])
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
    prepare_subset_vcf_files()


if __name__ == "__main__":
    main()
