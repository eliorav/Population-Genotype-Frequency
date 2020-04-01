import os
from glob import glob

import pandas as pd

from tqdm import tqdm

from constants import SNPS_DATA_PATH, SNPS_DATA_FOLDER, SNPS_DATA_FILE_NAME

from docker_runner import Hg38dbDockerRunner


def fetch_snps_data():
    if not os.path.exists(SNPS_DATA_PATH):
        print("retrieving SNPs data (chrom, position)")
        os.makedirs(SNPS_DATA_PATH)
        df = pd.read_csv('./allele_order.tsv', sep="\t", names=['snp', 'allele'])
        snps = df['snp'].unique()
        step_size = 500
        steps = int(len(snps) / step_size) + 1
        hg38db_docker_runner = Hg38dbDockerRunner()

        with tqdm(total=len(snps)) as pbar:
            for step in range(steps):
                start = step * step_size
                end = -1 if step == (steps - 1) else (step + 1) * step_size
                snps_query = '", "'.join(snps[start:end])
                pbar.set_description(f"Processing snps in range {start} - {end if end != -1 else len(snps)}")
                hg38db_docker_runner(environment={
                    'QUERY': f'select chrom, chromEnd, name from snp150 where name in ("{snps_query}")',
                    'FILE_NAME': f'{SNPS_DATA_FOLDER}/snps_data_{step}'
                })
                pbar.update(step_size if step != (steps - 1) else len(snps) - step * step_size)


def merge_snps_data():
    snps_files = glob(f"{SNPS_DATA_PATH}/*.csv")
    df = pd.concat([pd.read_csv(snps_file) for snps_file in snps_files], ignore_index=True)
    df = df[~df['chrom'].str.contains('alt')]
    df.sort_values(by=['chrom', 'chromEnd'], inplace=True)
    df.rename(columns={"chrom": "#chrom", "chromEnd": "position ", "name": "rsid"}, inplace=True)
    df.to_csv(f'{SNPS_DATA_PATH}/{SNPS_DATA_FILE_NAME}', index=False)
