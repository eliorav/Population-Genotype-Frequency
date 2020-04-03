import os
import pandas as pd
from constants import SAMPLES_FOLDER


def prepare_sample_data(args=None):
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
    else:
        print(f"Sample data already exist in {SAMPLES_FOLDER}")
