import os
import shutil
import argparse
from multiprocessing import Process
from services.prepare_freq_data import prepare_freq_data
from services.prepare_genotype_data import prepare_genotype_data
from services.prepare_population_vcf_data import prepare_subset_vcf_files_by_population
from services.prepare_sample_data import prepare_sample_data
from services.prepare_snps_data import prepare_snps_data
from constants import DATA_FOLDER, RESULT_FREQ_FILE_NAME, DEFAULT_OUT_FOLDER, DEFAULT_OUT_FILE_NAME, \
    DEFAULT_SNPS_LIST_PATH
from pathlib import Path


def main(args):
    """
    Main script
    :param args: script args
    """
    print(f"running the script with the following arguments: {args}")
    args.out_folder = Path(args.out_folder)

    parallel_steps = [prepare_sample_data, prepare_snps_data, prepare_genotype_data]

    if not args.no_parallel:
        processes = [Process(target=step, kwargs={
                             "args": args}) for step in parallel_steps]
        for process in processes:
            process.start()
        for process in processes:
            process.join()
    else:
        for step in parallel_steps:
            step(args)

    prepare_subset_vcf_files_by_population()
    prepare_freq_data()
    args.out_folder.mkdir(exist_ok=True, parents=True)
    shutil.copyfile(f'{DATA_FOLDER}/{RESULT_FREQ_FILE_NAME}',
                    args.out_folder/f"{args.out_filename}.freq")
    shutil.rmtree(DATA_FOLDER)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        "Create allele frequency by population file from 1000G data.")
    parser.add_argument('--out_folder', type=str, default=DEFAULT_OUT_FOLDER,
                        help=f'The output folder of the result file. The default is "output".')
    parser.add_argument('--out_filename', type=str, default=DEFAULT_OUT_FILE_NAME,
                        help=f'The output file name of the result file (without suffix). '
                             f'The default is "allele_frequency".')
    parser.add_argument('--snps_file_path', type=str, default=DEFAULT_SNPS_LIST_PATH,
                        help=f'The path to the list of SNPs - The default is "snps.tsv".')
    parser.add_argument('--no_parallel', type=bool, default=False,
                        help=f'If the value is true, the script will not run in parallel mode.')
    parser.add_argument('--pop_type', type=str, default='regular', choices=['regular', 'super_pop'],
                        help=f'The type of population to use. regular population or super population')
    main(parser.parse_args())
