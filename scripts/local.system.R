################################################################################
#                                  LOCAL SYSTEM                                #
################################################################################

### Operating System Version
### MacBook Pro
ROOT_loc = "/Users/slaan3"

### General
GENOMIC_loc = paste0(ROOT_loc, "/OneDrive - UMC Utrecht/Genomics")
AEDB_loc = paste0(GENOMIC_loc, "/Athero-Express/AE-AAA_GS_DBs")
LAB_loc = paste0(GENOMIC_loc, "/LabBusiness")

PROJECT_loc = paste0(ROOT_loc, "/git/CirculatoryHealth/AE_20211201_YAW_SWVANDERLAAN_HDAC9")

# Genetic and genomic data
STORAGE_loc = paste0(ROOT_loc, "/PLINK")
AERNA_loc = paste0(STORAGE_loc, "/_AE_ORIGINALS/AERNA")
AESCRNA_loc = paste0(STORAGE_loc, "/_AE_ORIGINALS/AESCRNA/prepped_data")
AEGSQC_loc = paste0(STORAGE_loc, "/_AE_ORIGINALS/AEGS_COMBINED_QC2018")
MICHIMP_loc=paste0(STORAGE_loc,"/_AE_ORIGINALS/AEGS_COMBINED_EAGLE2_1000Gp3v5HRCr11")

### SOME VARIABLES WE NEED DOWN THE LINE
TRAIT_OF_INTEREST = "HDAC9" # Phenotype
PROJECTNAME = "HDAC9"

cat("\nCreate a new analysis directory...\n")
ifelse(!dir.exists(file.path(PROJECT_loc, "/",PROJECTNAME)), 
       dir.create(file.path(PROJECT_loc, "/",PROJECTNAME)), 
       FALSE)
ANALYSIS_loc = paste0(PROJECT_loc,"/",PROJECTNAME)

ifelse(!dir.exists(file.path(ANALYSIS_loc, "/PLOTS")), 
       dir.create(file.path(ANALYSIS_loc, "/PLOTS")), 
       FALSE)
PLOT_loc = paste0(ANALYSIS_loc,"/PLOTS")

ifelse(!dir.exists(file.path(PLOT_loc, "/QC")), 
       dir.create(file.path(PLOT_loc, "/QC")), 
       FALSE)
QC_loc = paste0(PLOT_loc,"/QC")

ifelse(!dir.exists(file.path(ANALYSIS_loc, "/OUTPUT")), 
       dir.create(file.path(ANALYSIS_loc, "/OUTPUT")), 
       FALSE)
OUT_loc = paste0(ANALYSIS_loc, "/OUTPUT")

ifelse(!dir.exists(file.path(ANALYSIS_loc, "/BASELINE")), 
       dir.create(file.path(ANALYSIS_loc, "/BASELINE")), 
       FALSE)
BASELINE_loc = paste0(ANALYSIS_loc, "/BASELINE")

ifelse(!dir.exists(file.path(ANALYSIS_loc, "/COX")), 
       dir.create(file.path(ANALYSIS_loc, "/COX")), 
       FALSE)
COX_loc = paste0(ANALYSIS_loc, "/COX")


setwd(paste0(PROJECT_loc))
getwd()
list.files()