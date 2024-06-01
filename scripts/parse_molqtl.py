#!/usr/bin/env python3

# general libraries
import os
import importlib
import subprocess

# time and date
import time
from datetime import datetime, timedelta

# argument parsing
import argparse

# data manipulation
import polars as pl
from scipy import stats
import numpy as np

# plotting
import matplotlib.pyplot as plt
import seaborn as sns

# set the plotting style -- we are going to add this later
# import cmcrameri as ccm
# from cmcrameri import cm

# Version information
VERSION_NAME = 'Parse molQTL results'
VERSION = '1.1.0'
VERSION_DATE = '2024-05-31'
COPYRIGHT = 'Copyright 1979-2024. Sander W. van der Laan | s.w.vanderlaan [at] gmail [dot] com | https://vanderlaanand.science.'
COPYRIGHT_TEXT = '''
The MIT License (MIT).

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and 
associated documentation files (the "Software"), to deal in the Software without restriction, 
including without limitation the rights to use, copy, modify, merge, publish, distribute, 
sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is 
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies 
or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR 
PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS 
BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, 
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE 
OR OTHER DEALINGS IN THE SOFTWARE.

Reference: http://opensource.org.
'''

# Define colors
###	UtrechtSciencePark Colours Scheme
###
### Website to convert HEX to RGB: http://hex.colorrrs.com.
### For some functions you should divide these numbers by 255.
###
###	No.	Color				HEX		RGB							CMYK					CHR		MAF/INFO
### --------------------------------------------------------------------------------------------------------------------
###	1	yellow				#FBB820 (251,184,32)				(0,26.69,87.25,1.57) 	=>	1 		or 1.0 > INFO
###	2	gold				#F59D10 (245,157,16)				(0,35.92,93.47,3.92) 	=>	2		
###	3	salmon				#E55738 (229,87,56) 				(0,62.01,75.55,10.2) 	=>	3 		or 0.05 < MAF < 0.2 or 0.4 < INFO < 0.6
###	4	darkpink			#DB003F ((219,0,63)					(0,100,71.23,14.12) 	=>	4		
###	5	lightpink			#E35493 (227,84,147)				(0,63,35.24,10.98) 	=>	5 		or 0.8 < INFO < 1.0
###	6	pink				#D5267B (213,38,123)				(0,82.16,42.25,16.47) 	=>	6		
###	7	hardpink			#CC0071 (204,0,113)					(0,0,0,0) 	=>	7		
###	8	lightpurple			#A8448A (168,68,138)				(0,0,0,0) 	=>	8		
###	9	purple				#9A3480 (154,52,128)				(0,0,0,0) 	=>	9		
###	10	lavendel			#8D5B9A (141,91,154)				(0,0,0,0) 	=>	10		
###	11	bluepurple			#705296 (112,82,150)				(0,0,0,0) 	=>	11		
###	12	purpleblue			#686AA9 (104,106,169)				(0,0,0,0) 	=>	12		
###	13	lightpurpleblue		#6173AD (97,115,173/101,120,180)	(0,0,0,0) 	=>	13		
###	14	seablue				#4C81BF (76,129,191)				(0,0,0,0) 	=>	14		
###	15	skyblue				#2F8BC9 (47,139,201)				(0,0,0,0) 	=>	15		
###	16	azurblue			#1290D9 (18,144,217)				(0,0,0,0) 	=>	16		 or 0.01 < MAF < 0.05 or 0.2 < INFO < 0.4
###	17	lightazurblue		#1396D8 (19,150,216)				(0,0,0,0) 	=>	17		
###	18	greenblue			#15A6C1 (21,166,193)				(0,0,0,0) 	=>	18		
###	19	seaweedgreen		#5EB17F (94,177,127)				(0,0,0,0) 	=>	19		
###	20	yellowgreen			#86B833 (134,184,51)				(0,0,0,0) 	=>	20		
###	21	lightmossgreen		#C5D220 (197,210,32)				(0,0,0,0) 	=>	21		
###	22	mossgreen			#9FC228 (159,194,40)				(0,0,0,0) 	=>	22		or MAF > 0.20 or 0.6 < INFO < 0.8
###	23	lightgreen			#78B113 (120,177,19)				(0,0,0,0) 	=>	23/X
###	24	green				#49A01D (73,160,29)					(0,0,0,0) 	=>	24/Y
###	25	grey				#595A5C (89,90,92)					(0,0,0,0) 	=>	25/XY	or MAF < 0.01 or 0.0 < INFO < 0.2
###	26	lightgrey			#A2A3A4	(162,163,164)				(0,0,0,0) 	=> 	26/MT
### 
### ADDITIONAL COLORS
### 27	midgrey				#D7D8D7
### 28	very lightgrey		#ECECEC
### 29	white				#FFFFFF
### 30	black				#000000
### --------------------------------------------------------------------------------------------------------------------

uithof_color = ["#FBB820","#F59D10","#E55738","#DB003F","#E35493","#D5267B",
                 "#CC0071","#A8448A","#9A3480","#8D5B9A","#705296","#686AA9",
                 "#6173AD","#4C81BF","#2F8BC9","#1290D9","#1396D8","#15A6C1",
                 "#5EB17F","#86B833","#C5D220","#9FC228","#78B113","#49A01D",
                 "#595A5C","#A2A3A4", "#D7D8D7", "#ECECEC", "#FFFFFF", "#000000"]

# molQTL data directories 
# eQTL data directories
NOM_CIS_EQTL_loc = "/Users/slaan3/git/CirculatoryHealth/molqtl/results/version1_aernas1_firstrun/nom_cis_eqtl"
NOM_CIS_EQTL_SEX_loc = "/Users/slaan3/git/CirculatoryHealth/molqtl/results/version1_aernas1_firstrun/eqtl_gender"
NOM_CIS_EQTL_SEXINT_loc = "/Users/slaan3/git/CirculatoryHealth/molqtl/results/version1_aernas1_firstrun/sex_int_annot"
NOM_CIS_EQTL_SMOKING_loc = "/Users/slaan3/git/CirculatoryHealth/molqtl/results/version1_aernas1_firstrun/eqtl_smoking"
NOM_CIS_EQTL_SMOKINGINT_loc = "/Users/slaan3/git/CirculatoryHealth/molqtl/results/version1_aernas1_firstrun/smoking_int_annot"
PERM_TRANS_EQTL_loc = "/Users/slaan3/git/CirculatoryHealth/molqtl/results/version1_aernas1_firstrun/perm_trans_eqtl"

# mQTL data directories 
PERM_CIS_MQTL_loc = "/Users/slaan3/git/CirculatoryHealth/molqtl/results/perm_cis_mqtl"
PERM_TRANS_MQTL_loc = "/Users/slaan3/git/CirculatoryHealth/molqtl/results/perm_trans_mqtl"

# Reference and GWAS data directories 
REF_loc = "/Users/slaan3/PLINK/references"
GWAS_loc = "/Users/slaan3/PLINK/_GWAS_Datasets"

# Function to check if a package is installed and install it if it is not
def check_install_package(package_name):
    try:
        importlib.import_module(package_name)
    except ImportError:
        print(f'{package_name} is not installed. Installing it now...')
        subprocess.check_call(['pip', 'install', package_name])

# Function to merge and export molQTL results
def molqtl_merge_and_export(target_variants, sumstats, left_col, right_col, sort_column, output_csv, verbose=False, debug=False):
    if verbose:
        print(f'  > Starting merge of target variants with nominal cis-eQTLs.')
    temp = target_variants.join(sumstats, left_on=left_col, right_on=right_col, how="inner")    
    if verbose:
        print(f'  > Sorting the DataFrame by column "{sort_column}" in descending order.')
    result = temp.sort(sort_column)
    if debug:
        print(f'  > [DEBUG] Removing temporary DataFrame from memory.')
        del temp
    if verbose:
        print(f'  > Showing the first 5 rows of the DataFrame.')
        print(result)
    if verbose:
        print(f'  > Exporting the Polars DataFrame to a CSV file.')
    result.write_csv(output_csv)

# Main function
def main():

# Parse command-line arguments
    parser = argparse.ArgumentParser(description=f'''
+ {VERSION_NAME} v{VERSION} +

This script extracts molQTL results from the Athero-Express Biobank Study. 
The phenotype of interest is given by `--trait` and the project name is given by `--project_name`. 
As an example and by default, the script uses `PCSK9` as `--trait` and `--project_name`.

The script requires the genome build of the results (`--build`), which can be either b37 or b38. Currently, 
the script only supports b37. The script also requires the type of lookup to perform (`--analysis`), which can be
either `cise` (cis-eQTL, nominal), `cism` (cis-mQTL, permuted), `transe` (trans-eQTL, permuted), `transm` 
(trans-mQTL, permuted), or `all` (get all results). Currently, the script does not support the analysis types
`cisesmoking`, `cisesex`, `cisesmokingint`, and `cisesexint`.

The script can print extra information using the `--verbose` argument. 

The `--debug` argument prints debug information. Note: this creates a lot of output - think carefully.

The `--version` argument prints the version and exits the script.

Example usage:
    python parse_molqtl.py --trait PCSK9 --project_name PCSK9_project --build b37 --analysis cise --verbose
        ''',
        epilog=f'''
+ {VERSION_NAME} v{VERSION}. {COPYRIGHT} \n{COPYRIGHT_TEXT}+''', 
        formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument('--trait', '-t', type=str, default='PCSK9', help='Phenotype of interest (default: PCSK9). Required.')
    parser.add_argument('--project_name', '-p', type=str, default='PCSK9', help='Name of the project (default: PCSK9). Required.')
    parser.add_argument('--analysis', '-a', type=str, choices=['cise', 'transe', 'cism', 'transm', 'all', 'cisesmoking', 'cisesex', 'cisesmokingint', 'cisesexint'], help='Type of lookup to perform. (default: cise). Choices: cise (cis-eQTL, nominal), transe (trans-eQTL, permuted), cism (cis-mQTL, permuted), transm (trans-mQTL, permuted), all (get all results), cisesmoking (cis-eQTL, smoking), cisesex (cis-eQTL, sex), cisesmokingint (cis-eQTL, smoking interaction), cisesexint (cis-eQTL, sex interaction). Required.')
    parser.add_argument('--build', '-b', type=str, default='b37', choices=['b37', 'b38'], help='Genome build of the results. (default: b37). Choices: b37, b38. Required.')
    parser.add_argument('--verbose', '-v', action='store_true', help='Print extra information. Optional.')
    parser.add_argument('--debug', '-d', action='store_true', help='Print debug information. Note: this creates a lot of output - think carefully. Optional.')
    parser.add_argument('--version', '-V', action='version', version=f'%(prog)s {VERSION} ({VERSION_DATE}).')
    args = parser.parse_args()

    # Start the timer
    start_time = time.time()

    # Get today's date
    today_date = datetime.now()

    # Start the script
    print(f"+ {VERSION_NAME} v{VERSION} ({VERSION_DATE}) +")
    print(f"\nStarting extraction job {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.")

    # Check if required arguments are provided
    required_args = ['trait', 'project_name', 'analysis', 'build']
    missing_args = [arg for arg in required_args if not getattr(args, arg)]
    if missing_args:
        print(f"Error. The following required arguments are missing: {', '.join(missing_args)}.\n")
        print(f"Please provide the required arguments, as shown below.\n")
        parser.print_help()
        exit(1)
    if args.build == 'b38':
        print(f"Error. The script only supports b37 at the moment. Please provide the correct genome build.\n")
        print(f"Please provide the required arguments, as shown below.\n")
        parser.print_help()
        exit(1)
    if args.analysis == 'cisesmoking' or args.analysis == 'cisesex' or args.analysis == 'cisesmokingint' or args.analysis == 'cisesexint':
        print(f"Error. The script does not support the analysis type '{args.analysis}' at the moment. Please provide the correct analysis type.\n")
        print(f"Please provide the required arguments, as shown below.\n")
        parser.print_help()
        exit(1)

    # Print extra information 
    print(f"Trait................... {args.trait}")
    print(f"Project name............ {args.project_name}")
    print(f"Analysis type........... {args.analysis}")
    print(f"Genome build............ {args.build}")
    print(f"Verbose mode............ {'On' if args.verbose else 'Off (default)'}")
    print(f"Debug mode.............. {'On' if args.debug else 'Off (default)'}")
    print(f"Running version......... {VERSION} ({VERSION_DATE})")
    print(f"Running on.............. {today_date}\n\n")

    # Set some general defaults
    TRAIT_OF_INTEREST = args.trait
    PROJECTNAME = args.project_name
    BUILD = args.build
    # PLOTS_loc = "PLOTS"
    molQTL_loc = "molQTL_results"

    # Get today's date
    today_date = datetime.now()
    FORMATTED_TODAY = today_date.strftime("%Y%m%d")

    # Create directories if they don't exist
    # for directory in [molQTL_loc, PLOTS_loc]:
    for directory in [molQTL_loc]:
        if args.verbose:
            print(f'Creating the directory (if it did not exist): {directory}')
        if not os.path.exists(directory):
            os.makedirs(directory)

    # Check contents of reference and GWAS directories
    if args.debug:
        print(f'Checking contents of the reference directory:')
        print(os.listdir(REF_loc))
        print(f'Checking contents of the GWAS directory:')
        print(os.listdir(GWAS_loc))

    # Check contents of molQTL data directories
    if args.debug:
        print(f'[DEBUG] Checking contents of the molQTL data directories.')
        for directory in [NOM_CIS_EQTL_loc, PERM_CIS_MQTL_loc, PERM_TRANS_EQTL_loc, PERM_TRANS_MQTL_loc]:
            print(f'Checking contents of the directory: {directory}')
            print(os.listdir(directory))

    # Load the list of variants of interest for this project
    print(f'\n> Loading the list of variants of interest for the project. All the columns in this file are joined with the molQTL results.')
    target_variants = pl.read_excel(source=os.path.join("targets/targets.xlsx"), sheet_name="Variants")
    if args.verbose:
        print(f'  > Showing the first 5 rows of the Target list.')
        print(target_variants)

    # Load nominal cis-eQTL data
    if args.analysis == 'cise' or args.analysis == 'all':
        print(f'\n> Loading nominal cis-eQTL data.')
        sumstats_nom_cis_eqtl = pl.read_parquet(source=os.path.join(NOM_CIS_EQTL_loc, "tensorqtl_nominal_cis_qtl_pairs.annot.parquet"))

        # Merge and export nominal cis-eQTL data
        print(f'\n> Merging and exporting nominal cis-eQTL data.')
        nom_cis_eqtl_out_file=os.path.join(molQTL_loc, FORMATTED_TODAY + "." + PROJECTNAME + "." + BUILD + "." + TRAIT_OF_INTEREST + ".nom_cis_eqtl.csv")
        molqtl_merge_and_export(target_variants, sumstats_nom_cis_eqtl, "VariantID", "VariantID", "pval_nominal", nom_cis_eqtl_out_file, verbose=args.verbose, debug=args.debug)

        # Clean up
        if args.debug:
            print(f'[DEBUG] Removing the nominal cis-eQTL data from memory.')
        del sumstats_nom_cis_eqtl

    # Load nominal cis-mQTL data
    if args.analysis == 'cism' or args.analysis == 'all':
        print(f'\n> Loading nominal cis-mQTL data.')
        file_path_perm_cis_mqtl = os.path.join(PERM_CIS_MQTL_loc, "tensormqtl.perm_cis_mqtl.txt")
        sumstats_perm_cis_mqtl = pl.read_csv(file_path_perm_cis_mqtl, has_header=True, separator="\t", ignore_errors=True)

        # Merge and export nominal cis-mQTL data
        print(f'\n> Merging and exporting nominal cis-mQTL data.')
        perm_cis_mqtl_out_file=os.path.join(molQTL_loc, FORMATTED_TODAY + "." + PROJECTNAME + "." + BUILD + "." + TRAIT_OF_INTEREST + ".perm_cis_mqtl.csv")
        molqtl_merge_and_export(target_variants, sumstats_perm_cis_mqtl, "VariantID", "variant_id", "pval_nominal", perm_cis_mqtl_out_file, verbose=args.verbose, debug=args.debug)

        # Clean up
        if args.debug:
            print(f'[DEBUG] Removing the nominal cis-mQTL data from memory.')
        del sumstats_perm_cis_mqtl

    # Load nominal trans-eQTL data
    if args.analysis == 'transe' or args.analysis == 'all':
        print(f'\n> Loading the permuted trans-eQTL data.')
        file_path_perm_trans_eqtl = os.path.join(PERM_TRANS_EQTL_loc, "tensorqtl_trans_full.trans_qtl_pairs.parquet")
        sumstats_perm_trans_eqtl = pl.read_parquet(file_path_perm_trans_eqtl)

        # Merge and export nominal trans-eQTL data
        print(f'\n> Merging and exporting the permuted trans-eQTL data.')
        perm_trans_eqtl_out_file=os.path.join(molQTL_loc, FORMATTED_TODAY + "." + PROJECTNAME + "." + BUILD + "." + TRAIT_OF_INTEREST + ".perm_trans_eqtl.csv")
        molqtl_merge_and_export(target_variants, sumstats_perm_trans_eqtl, "VariantID", "variant_id", "pval", perm_trans_eqtl_out_file, verbose=args.verbose, debug=args.debug)

        # Clean up
        if args.debug:
            print(f'[DEBUG] Removing the permuted trans-eQTL data from memory.')
        del sumstats_perm_trans_eqtl

    # Load nominal trans-mQTL data
    if args.analysis == 'transm' or args.analysis == 'all':
        print(f'\n> Loading the permuted trans-mQTL data.')
        file_path_perm_trans_mqtl = os.path.join(PERM_TRANS_MQTL_loc, "tensormqtl_perm_trans_qtl_pairs.annot.parquet")
        sumstats_perm_trans_mqtl = pl.read_parquet(file_path_perm_trans_mqtl)

        # Merge and export nominal trans-mQTL data
        print(f'\n> Merging and exporting the permuted trans-mQTL data.')
        perm_trans_mqtl_out_file=os.path.join(molQTL_loc, FORMATTED_TODAY + "." + PROJECTNAME + "." + BUILD + "." + TRAIT_OF_INTEREST + ".perm_trans_mqtl.csv")
        molqtl_merge_and_export(target_variants, sumstats_perm_trans_mqtl, "VariantID", "VariantID", "pval_perm", perm_trans_mqtl_out_file, verbose=args.verbose, debug=args.debug)

        # Clean up
        if args.debug:
            print(f'[DEBUG] Removing the permuted trans-mQTL data from memory.')
        del sumstats_perm_trans_mqtl

    # Calculate and print execution time
    elapsed_time = time.time() - start_time
    time_delta = timedelta(seconds=elapsed_time)
    formatted_time = str(time_delta).split('.')[0]
    print(f"Script executed on {today_date.strftime('%Y-%m-%d')}. Total execution time: {formatted_time}.")

    # Print the version and license information
    print(f"\n+ {VERSION_NAME} v{VERSION} ({VERSION_DATE}). {COPYRIGHT} +")
    print(COPYRIGHT_TEXT)

if __name__ == "__main__":
    main()
# End of file