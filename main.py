from services.prepare_freq_data import prepare_freq_data
from services.prepare_population_vcf_data import prepare_subset_vcf_files_by_population
from services.prepare_sample_data import prepare_sample_data
from services.prepare_snps_data import prepare_snps_data


def main():
    """
    Main script
    """
    prepare_sample_data()
    prepare_snps_data()
    prepare_subset_vcf_files_by_population()
    prepare_freq_data()


if __name__ == "__main__":
    main()
