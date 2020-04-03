# FOLDERS
DATA_FOLDER = '.data2'
VCF_BY_POPULATION_FOLDER = 'vcf_by_population'
FREQ_BY_POPULATION_FOLDER = 'freq_by_population'
SNPS_DATA_FOLDER = 'SNPs_data'
SAMPLES_FOLDER = f'{DATA_FOLDER}/samples'
SNPS_DATA_FILE_NAME = 'snps_data_all.csv'
RESULT_FREQ_FILE_NAME = 'result.freq'
GENOTYPE_DATA_FOLDER = 'genotype_data'
MERGED_GENOTYPE_FILE = 'all_phase3'
MERGED_VCF_FILE_NAME = f'{MERGED_GENOTYPE_FILE}.vcf'
SNP_LIST_FILE_NAME = 'snps.tsv'
DEFAULT_OUT_FOLDER = 'output'
DEFAULT_OUT_FILE_NAME = 'allele_frequency'
DEFAULT_SNPS_LIST_PATH = 'snps.tsv'

# PATHS
VCF_BY_POPULATION_PATH = f'{DATA_FOLDER}/{VCF_BY_POPULATION_FOLDER}'
FREQ_BY_POPULATION_PATH = f'{DATA_FOLDER}/{FREQ_BY_POPULATION_FOLDER}'
SNPS_DATA_PATH = f'{DATA_FOLDER}/{SNPS_DATA_FOLDER}'
GENOTYPE_DATA_PATH = f'{DATA_FOLDER}/{GENOTYPE_DATA_FOLDER}'
MERGED_VCF_OUTPUT_PATH = f'{GENOTYPE_DATA_PATH}/{MERGED_VCF_FILE_NAME}'

# DOCKER IMAGES
IMAGE_WORKDIR = '/usr/src/app/'
IMAGE_SHARE_FOLDER_PATH = f'{IMAGE_WORKDIR}share_folder'
VCF_TOOLS_IMAGE_NAME = 'avelior/vcftools'
PLINK2_IMAGE_NAME = 'avelior/plink2'
HG38DB_IMAGE_NAME = 'avelior/hg38db'

# VCF
PSAM_PATH = 'https://www.dropbox.com/s/yozrzsdrwqej63q/phase3_corrected.psam?dl=1'
PVAR_PATH = 'https://www.dropbox.com/s/op9osq6luy3pjg8/all_phase3.pvar.zst?dl=1'
PGEN_PATH = 'https://www.dropbox.com/s/afvvf1e15gqzsqo/all_phase3.pgen.zst?dl=1'
