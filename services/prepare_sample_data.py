import os
import pandas as pd
from constants import SAMPLES_FOLDER


def prepare_sample_data(args=None):
    """
    Extract samples data for each population to a file
    """
    if not SAMPLES_FOLDER.exists():
        SAMPLES_FOLDER.mkdir(exist_ok=True, parents=True)
        population_field = 'pop' if args.pop_type == 'regular' else 'super_pop'
        all_samples_df = pd.read_csv('./integrated_call_samples.ALL.panel', sep="\t")
        populations = all_samples_df[population_field].unique()

        for pop in populations:
            pop_df = all_samples_df[all_samples_df[population_field] == pop]['sample']
            pop_df.to_csv(SAMPLES_FOLDER/f'{pop}.samples.csv', header=False, index=False, sep='\t')
    else:
        print(f"Sample data already exist in {SAMPLES_FOLDER}")
