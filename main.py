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


def main(args):
    """
    Main script
    :param args: script args
    """
    print(f"running the script with the following arguments: {args}")
    parallel_steps = [prepare_sample_data, prepare_snps_data, prepare_genotype_data]

    if not args.no_parallel:
        processes = [Process(target=step, kwargs={"args": args}) for step in parallel_steps]
        for process in processes: process.start()
        for process in processes: process.join()
    else:
        for step in parallel_steps: step(args)

    prepare_subset_vcf_files_by_population()
    prepare_freq_data()
    if not os.path.exists(args.out_folder):
        os.makedirs(args.out_folder)
    shutil.copyfile(f'{DATA_FOLDER}/{RESULT_FREQ_FILE_NAME}', f"{args.out_folder}/{args.out_filename}.freq")
    shutil.rmtree(DATA_FOLDER)


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser("Create allele frequency by population file from 1000G data.")
    PARSER.add_argument('--out_folder', type=str, default=DEFAULT_OUT_FOLDER,
                        help=f'The output folder of the result file. The default is "output".')
    PARSER.add_argument('--out_filename', type=str, default=DEFAULT_OUT_FILE_NAME,
                        help=f'The output file name of the result file (without suffix). '
                             f'The default is "allele_frequency".')
    PARSER.add_argument('--snps_file_path', type=str, default=DEFAULT_SNPS_LIST_PATH,
                        help=f'The path to the list of SNPs - The default is "snps.tsv".')
    PARSER.add_argument('--no_parallel', type=bool, default=False,
                        help=f'If the value is true, the script will not run in parallel mode.')
    main(PARSER.parse_args())
