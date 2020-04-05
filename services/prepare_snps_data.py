import os
from glob import glob
import pandas as pd
from tqdm import tqdm
from constants import SNPS_DATA_PATH, SNPS_DATA_FOLDER, SNPS_DATA_FILE_NAME
from services.docker_runner import Hg38dbDockerRunner


def fetch_snps_data(snps_file_path):
    """
    Fetch SNPs data from hg38 db
    :param snps_file_path: the path of the SNPs list
    """
    print("retrieving SNPs data (chrom, position)")
    snps_df = pd.read_csv(snps_file_path, sep="\t", names=['snp', 'allele'])
    snps = snps_df['snp'].unique()
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
    """
    Merge the multiple files from hg38 db to a single file
    """
    print("merge SNPs data to a single file")
    snps_files = glob(f"{SNPS_DATA_PATH}/*.csv")
    snps_df = pd.concat([pd.read_csv(snps_file) for snps_file in snps_files], ignore_index=True)
    snps_df = snps_df[~snps_df['chrom'].str.contains('alt')]
    snps_df.sort_values(by=['chrom', 'chromEnd'], inplace=True)
    snps_df.rename(columns={"chrom": "#chrom", "chromEnd": "position", "name": "rsid"}, inplace=True)
    snps_df.to_csv(f'{SNPS_DATA_PATH}/{SNPS_DATA_FILE_NAME}', index=False)


def prepare_snps_data(args):
    """
    Prepare SNPs data
    :param args: script args - should include snps_file_path - the path of the SNPs list
    """
    if not os.path.exists(SNPS_DATA_PATH):
        os.makedirs(SNPS_DATA_PATH)
        fetch_snps_data(args.snps_file_path)
        merge_snps_data()
    else:
        print(f"SNPs data: {SNPS_DATA_PATH} already exist")
