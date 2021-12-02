# Lookup Template

> This is a "Lookup request" template. The naming of the repository should follow the convention we use in > Trello, _etc._, _e.g._ "AE_20190910_008_JHILLEBRANDS_SDEJAGER_TEMS_TIE2".
> 
> This template will probably be extended as we get more experienced. For instance, with some standard > codes/scripts for:
> 
> - SNP lookups
> - bulk RNAseq analyses
> - baseline tables
> - scRNAseq projections and lookups

# Mapping common variants to atherosclerotic plaques characteristics.

*Collaborators*

[First name] [Initials] [Last name]
[First name] [Initials] [Last name]
[First name] [Initials] [Last name]

*Athero-Express Team*

Sander W. van der Laan, 
Arjan Boltjes, 
Michal Mokry, 
Hester den Ruijter, 
Folkert W. Asselbergs, 
Gert Jan de Borst, 
Gerard Pasterkamp.

**Project ID** [`AE_[YYYYMMDD]_[PROJECTNUMBER]_[LEADCOLLABORATOR]_[PROJECTNAME]`]


## Background

Collaboration to study common variants in relation to atherosclerotic plaques characteristics. 


## Study design

We will test the hypothesis that common variants in a gene-of-interest are associated with plaque characteristics. We will use data from the **Athero-Express Biobank Study**.

These are the questions we will address: 

- Are any of the variants associated to plaque characteristics?
- Gene expression correlated to characteristics of plaques?
- Where target genes expressed, which cell types? 


### Athero-Express Biobank Study

We have bulk RNAseq (n = 635 samples) and single-cell RNAseq data, genome-wide methylation (Illumina 450K) in n ± 600, as well as overlapping genetic data for ±2,100 individuals with extensive histological plaque characterisation. 


### Genetic analyses

For the genetic analyses we will perform regression analyses adjusted for age, sex (where applicable) and principal components. So, we will apply the following model:

We will perform regression analyses adjusted for age, sex (where applicable) and principal components. 

model 1: `phenotype ~ age + sex + chip-used + PC1 + PC2 + year-of-surgery`

We can also run sex-stratified analyses:

model 1m: `phenotype ~ age + chip-used + PC1 + PC2 + year-of-surgery` males only
model 1f: `phenotype ~ age + chip-used + PC1 + PC2 + year-of-surgery` females only

phenotypes are:

- `calcification`, coded `Calc.bin` no/minor vs. moderate/heavy staining
- `collagen`, coded `Collagen.bin` no/minor vs. moderate/heavy staining
- `fat10`, coded `Fat.bin_10` no/<10% fat vs. >10% fat
- `fat40`, coded `Fat.bin_40` no/<40% fat vs. >40% fat
- `intraplaque hemorrhage`, coded `IPH.bin` no vs. yes
- `macrophages (CD68)`, coded `macmean0` mean of computer-assisted calculation CD68<sup>+</sup> region of interest
- `smooth muscle cells (alpha-actin)`, coded `smcmean0` mean of computer-assisted calculation SMA<sup>+</sup> region of interest
- `intraplaque vessel density (CD34)`, coded `vessel_density` manually counted CD34<sup>+</sup> cells per 3-4 hotspots
- `mast cells`, coded `Mast_cells_plaque` manually counted mast cell tryptase<sup>+</sup> cells (https://academic.oup.com/eurheartj/article/34/48/3699/484981) [Note: low sample size]
- `neutrophils (CD66b)`, coded `neutrophils` manually counted CD66b<sup>+</sup> cells (https://pubmed.ncbi.nlm.nih.gov/20595650/) [Note: low sample size]
- `plaque vulnerability index`, scaled from 0 to 4, where 0 is most stable, and 4 is least stable plaque phenotype.

Continuous variables were inverse-rank normal transformated, indicated by `_rankNorm`. 

**Figure 1: Genotyped individuals in the Athero-Express Biobank Study**
![Genotyped individuals in the Athero-Express Biobank Study](SOME_FANCY_PROJECTNAME/PLOTS/20210929.overlap.AEDB_AEGS123.UpSetR.png)


### Whole-plaque RNAseq

For the expression analysis we used carotid plaque-derived bulk RNAseq data and queried it for the gene list. Below a graph showing the overall expression of the genes (not all are in the data) compared to the mean expression of 1,000 randomly picked genes. 

**Figure 2: Overall expression of target genes in carotid plaques from the Athero-Express Biobank Study**
![Overall expression of target genes in carotid plaques from the Athero-Express Biobank Study](bulkRNAseq/AERNA/PLOTS/20210929.TargetExpression_vs_1000genes.png)

We assessed the correlation with plaque characteristics (mentioned above) and secondary major adverse cardiovascular events (MACE [major]) at 30 days and 3 years after CEA. 


### Single cell RNAseq

We projected target genes to the single-cell RNAseq data derived from 37 carotid plaque samples. We identified cell communities (Figure 2), mapped and projected target gene expression to the cell communities (Figure 3). 

**Figure 3: Cell communities identified in carotid plaques from the Athero-Express Biobank Study**
![Cell communities identified in carotid plaques from the Athero-Express Biobank Study](scRNAseq/AESCRNA/PLOTS/20210929.UMAP.png)


**Figure 4: Dotplot showing expression of target genes per cell type in carotid plaques from the Athero-Express Biobank Study**
![Dotplot showing expression of target genes per cell type in carotid plaques from the Athero-Express Biobank Study](scRNAseq/AESCRNA/PLOTS/20210929.DotPlot.Targets.png)


## Where do I start?

You can load this project in RStudio by opening the file called 'AE_TEMPLATE.Rproj'.

## Project structure

<!--  You can add rows to this table, using "|" to separate columns.         -->
File                       | Description                         | Usage         
-------------------------- | ----------------------------------- | --------------
README.md                  | Description of project              | Human editable
AE_TEMPLATE.Rproj          | Project file                        | Loads project
LICENSE                    | User permissions                    | Read only
.worcs                     | WORCS metadata YAML                 | Read only
renv.lock                  | Reproducible R environment          | Read only
images                     | image directory for project         | Human editable
bulkRNAseq                 | bulkRNAseq analysis directory       | Human editable
scRNAseq                   | scRNAseq analysis directory         | Human editable
SNP                        | SNP analysis directory              | Human editable
SOME_FANCY_PROJECTNAME     | Some results                        | Human editable
scripts                    | Scripts directory                   | Human editable

<!--  You can consider adding the following to this file:                    -->
<!--  * A citation reference for your project                                -->
<!--  * Contact information for questions/comments                           -->
<!--  * How people can offer to contribute to the project                    -->
<!--  * A contributor code of conduct, https://www.contributor-covenant.org/ -->

# Reproducibility

This project uses the Workflow for Open Reproducible Code in Science (WORCS) to
ensure transparency and reproducibility. The workflow is designed to meet the
principles of Open Science throughout a research project. 

To learn how WORCS helps researchers meet the TOP-guidelines and FAIR principles,
read the preprint at https://osf.io/zcvbs/

## WORCS: Advice for authors

* To get started with `worcs`, see the [setup vignette](https://cjvanlissa.github.io/worcs/articles/setup.html)
* For detailed information about the steps of the WORCS workflow, see the [workflow vignette](https://cjvanlissa.github.io/worcs/articles/workflow.html)

## WORCS: Advice for readers

Please refer to the vignette on [reproducing a WORCS project]() for step by step advice.
<!-- If your project deviates from the steps outlined in the vignette on     -->
<!-- reproducing a WORCS project, please provide your own advice for         -->
<!-- readers here.                                                           -->

# References

- Brown et al. (1979). Receptor-mediated endocytosis: insights from the lipoprotein receptor system. Proc Nat Acad Sci 76:3330–7.
- Brown et al. (1979). Reversible accumulation of cholesteryl esters in macrophages incubated with acetylated lipoproteins. J Cell Biol 82:597–613.
- Malik R,…(168 coauthors)…, Dichgans M (2018). Multi-ancestry genome-wide association study of 520,000 subjects identifies 32 loci associated with stroke and stroke subtypes. Nat Genet 50(4):524-537.
- Murshid et al. (2015) Emerging roles for scavenger receptor SREC-I in immunity. Cytokine 75(2):256-60.
- Ramirez-Ortiz et al. (2013). The scavenger receptor SCARF1 mediates the clearance of apoptotic cells and prevents autoimmunity. Nat immunol 14(9):917-26.


# Acknowledgements

Dr. Sander W. van der Laan is funded through grants from the Netherlands CardioVascular Research Initiative of the Netherlands Heart Foundation (CVON 2011/B019 and CVON 2017-20: Generating the best evidence-based pharmaceutical targets for atherosclerosis [GENIUS I&II]). We are thankful for the support of the ERA-CVD program ‘druggable-MI-targets’ (grant number: 01KL1802), the EU H2020 TO_AITION (grant number: 848146), and the Leducq Fondation ‘PlaqOmics’.

Plaque samples are derived from carotid endarterectomies as part of the [Athero-Express Biobank Study](http:www/atheroexpress.nl) which is an ongoing study in the UMC Utrecht.

The framework was based on the [`WORCS` package](https://osf.io/zcvbs/).

<a href='https://www.era-cvd.eu'><img src='images/ERA_CVD_Logo_CMYK.png' align="center" height="75" /></a> <a href='https://www.plaqomics.com'><img src='images/leducq-logo-large.png' align="center" height="75" /></a> <a href='https://www.fondationleducq.org'><img src='images/leducq-logo-small.png' align="center" height="75" /></a> <a href='https://osf.io/zcvbs/'><img src='images/worcs_icon.png' align="center" height="75" /></a> <a href='https://www.atheroexpress.nl'><img src='images/AE_Genomics_2010.png' align="center" height="100" /></a>

#### Changes log
    
    _Version:_      v1.1.0</br>
    _Last update:_  2021-09-29</br>
    _Written by:_   Sander W. van der Laan (s.w.vanderlaan-2[at]umcutrecht.nl).
        
    * v1.1.0 Major update to WORCS system. 
    * v1.0.6 Small bug fixes. 
    * v1.0.5 Added png for overlap-figure.
    * v1.0.5 Removed obsolete references to objects.
    * v1.0.4 Fixed a mistake in the chr X sample-file creation. Now the order matches the chr X data.
    * v1.0.3 Fixed weight of files (limit of 10Mb per file for templates). Renamed entire repo.
    * v1.0.2 Added sex-specific .sample-files. Added GWASToolKit input-files.
    * v1.0.0 Initial version. Add 'plaque vulnerability index', Fixed baseline table, added codes, and results. Created sample-files. 

--------------

#### Creative Commons BY-NC-ND 4.0
##### Copyright (c) 1979-2021 Sander W. van der Laan | s.w.vanderlaan [at] gmail [dot] com.

This is a human-readable summary of (and not a substitute for) the [license](LICENSE). 

You are free to: 
Share — copy and redistribute the material in any medium or format. The licensor cannot revoke these freedoms as long as you follow the license terms.

Under the following terms: 
- Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use. 
- NonCommercial — You may not use the material for commercial purposes. 
- NoDerivatives — If you remix, transform, or build upon the material, you may not distribute the modified material. 
- No additional restrictions — You may not apply legal terms or technological measures that legally restrict others from doing anything the license permits.

Notices: 
You do not have to comply with the license for elements of the material in the public domain or where your use is permitted by an applicable exception or limitation.
No warranties are given. The license may not give you all of the permissions necessary for your intended use. For example, other rights such as publicity, privacy, or moral rights may limit how you use the material.




