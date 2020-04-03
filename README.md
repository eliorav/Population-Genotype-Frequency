<p align="center">
  <h3 align="center">Population Genotype Frequency</h3>
  <p align="center">
    A Python script that generate population genotype frequency file from 1000G data
  </p>
</p>

## Built with
The script uses the following platform to run:
* [Python 3.6 +](https://www.python.org/)
* [Docker](https://www.docker.com/)
Make sure that you have those before running the script.

In order to run a linux only tools in every environment, the script uses the following docker wrappers:
* [avelior/plink2](https://github.com/eliorav/Biology-Tools/tree/master/plink2)
* [avelior/VCFtools](https://github.com/eliorav/Biology-Tools/tree/master/VCFtools)

## Script workflow
* step 1 - split every population's sample to a different file.
for example:
```sh
grep CEU integrated_call_samples.20101123.ALL.panel | cut -f1 > CEU.samples.list
``` 
* step 2 - add more information about the SNPs - add position to the given rsid.
* step 3 - get genotype data of 1000G phase3
    * download pgen pvar and psam of the merged dataset from [cog-genomics](http://www.cog-genomics.org/plink/2.0/resources#1kg_phase3) (the bold links).
    * decompress the pgen and the pvar files. for example:
    ```sh
    plink2 --zst-decompress all_phase3.pgen.zst > all_phase3.pgen
    ```
    * create 1000G merged dataset VCF file by using this command:
    ```sh
    plink2 --pfile all_phase3 vzs --extract [your list of rsIDs] --export vcf
    ``` 
* step 4 - Split the merged VCF file into multiple VCF files by population as describe [here](https://www.internationalgenome.org/faq/how-can-i-get-allele-frequency-my-variant/).
    * using the following command:
    ```sh
    vcf-subset -c [population sample list file] [merged VCF file] | fill-an-ac > [VCF by population output file]
    ```
* step 5 - create frequency files.
    * create a frequency file for every population by using this command:
    ```sh
    plink2 --vcf [VCF by population file] --freq --out [frequency by population output file]
    ```
    * merge the frequency files to a single one file and add the RSID and the position to the final file.
* step 6 - cleanup the temp files.
Note that steps 1-3 can run in parallel.
 
## Getting Started
### Prerequisites
Install requirements libraries
```sh
pip install --user -r requirements.txt
```

### Usages
you can run the script with `-h` flag to see the supporting arguments:
```sh
python main.py -h
```
returns the following:
```sh
usage: Create allele frequency by population file from 1000G data
       [-h] [--out_folder OUT_FOLDER] [--out_filename OUT_FILENAME]
       [--snps_file_path SNPS_FILE_PATH] [--no_parallel NO_PARALLEL]

optional arguments:
  -h, --help            show this help message and exit
  --out_folder OUT_FOLDER
                        The output folder of the result file. The default is "output".
  --out_filename OUT_FILENAME
                        the output file name of the result file (without suffix). The default is "allele_frequency".
  --snps_file_path SNPS_FILE_PATH
                        The path to the list of SNPs - The default is "snps.tsv".
  --no_parallel NO_PARALLEL
                        If the value is true, The script will not run in parallel mode.

```

Make sure to create an RSID list and pass the path to the script.

### Output
The output file is a TSV file with the following header:
* \#chrom - the chromosome number.
* position - the position of the SNP.
* rsid - the RSID number.
* A1 - the REF allele.
* A2 - the ALT allele.
* POOPULATION_NAME (e.g., ACB) - the frequency for the SNP in the given population.
The file is sorted by chromosome and position.

## Contact
Elior Avraham – elior.av@gmail.com

