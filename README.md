<div><img src="https://github.com/yzerlaut/datavyz/raw/master/docs/logo.png" alt="datavyz logo" width="45%" align="right" style="margin-left: 10px"></div>

# finalyz

*A plain text (.txt)-based framework to efficiently describe methods and results in scientific communications.*

Part of the software suite for data science: [analyz](https://github.com/yzerlaut/analyz), [datavyz](https://github.com/yzerlaut/datavyz), [finalyz](https://github.com/yzerlaut/finalyz)

## Idea / Principle

What this software enables is to:
- Provide a datafile (e.g. a python dictionary file "data.npz") and have your numerical values exported automatically within the text (no need to manually copy-paste the analysis output).
- Export your analysis to the document format that best fits your audience !
   - either short reports with two columns
   - either long and detailed reports in the single column 
   - either to pre-defined templates of scientific journals: PloS journals, Springer journals, Physical Review journals, Cell journals, J. Neurosci., etc ...
- Bibliographic export 
- Benefit from the the Emacs editing capabilities (the txt template uses the Org-Mode syntax).

## Installation

Clone the repository and `source` the main script with:
```
git clone https://github.com/yzerlaut/finalyz
source finalyz/run.sh
```

## User guide

Work on your "txt" file (see the templates in the [template folder](https://github.com/yzerlaut/finalyz/tree/master/templates) and compile it with:

```
finalyz you_paper.txt
```
or alternatively
```
report you_paper.txt # shortcut for a report
```

## Including quantitative results

We show here how to use cross-referencing with respect to an analysis file to generate report the results of the study. In this demo case (generated in the (https://github.com/yzerlaut/finalyz/blob/master/docs/notebook.ipynb)[documentation notebook], the (https://github.com/yzerlaut/finalyz/raw/master/study.npz)[study.npz] file contains both study parameters and analysis results:

```
{'Nobs': 5,
 'Nsample': 100,
 'cc_coef_over_obs_max': 0.223,
 'cc_coef_over_obs_mean': 0.055,
 'cc_coef_over_obs_min': -0.122,
 'cc_coef_over_obs_std': 0.103,
 'cc_pval_over_obs_max': 0.856,
 'cc_pval_over_obs_min': 0.026,
 'mean_value': 1.605,
 'sem_value': 0.13,
 'study_duration': '2 months'}
```

we use the syntax (using python's dictionary replacement syntax):

```
The study was conducted over {study_duration}. It contained {Nsample} of {Nobs} observations. Signal was: {mean_value} $\pm$ {sem_value}. Cross-correlation over observations was {cc_coef_over_obs_mean} $\pm$ {cc_coef_over_obs_mean} with minimum {cc_coef_over_obs_min} and maximum {cc_pval_over_obs_max}.
P-values of linear correlation spanned a range between pval={cc_pval_over_obs_min} and pval={cc_pval_over_obs_max}
```

are exported to:

> The study was conducted over 2 months. It contained 100 of 5 observations. Signal was: 1.605 ± 0.13. Cross- correlation over observations was 0.055 ± 0.055 with minimum -0.122 and maximum 0.856. P-values of linear correlation spanned a range between pval=0.026 and pval=0.856.

## References

Reference are included in the text by a plain text citation style:

```
A landwark study on visual cortex (Hubel and Wiesel, 1962)
```

that should point to a bibtex entry in the `References` section:
```
* References

@article{Hubel_and_Wiesel_1962,
  title={Receptive fields, binocular interaction and functional architecture in the cat's visual cortex},
  author={Hubel, David H and Wiesel, Torsten N},
  journal={The Journal of physiology},
  volume={160},
  number={1},
  pages={106--154},
  year={1962},
  publisher={Wiley Online Library}
}
```
The compiled citation will depend on the citation style used.
- For:
```
finalyz your_paper.txt --citation_style text # default settings
```
> A landwark study on visual cortex (Hubel and Wiesel, 1962)

- For:
```
finalyz your_paper.txt --citation_style number
```
> A landwark study on visual cortex [1]

- For:
```
finalyz your_paper.txt --citation_style exponent_number
```
> A landwark study on visual cortex^1


## Equations

## Manuscript informations

The set of manuscript informations are:

- Title
- Short title
- Authors
- Short authors
- Affiliations
- Correspondance
- Keywords
- Conflict of interest
- Acknowledgements
- Funding

They can be set up either in the preamble, e.g. as:

```
#+Title: A template for scientific papers
#+Authors: First Author{1}, Second Author{1,2}*
#+Short title: Paper Template
#+Short authors: Author et al.
#+Affiliations: {1} My first affiliation, {2} Second author affiliation
#+Conflict of interest: The authors declare no conflict of interest
```

or in the information section as:

```
* Informations
*** Title
A template for scientific papers

*** Authors
First Author{1}, Second Author{1,2}*

*** Short title
Paper Template

*** Short authors
Author et al.

*** Affiliations
{1} My first affiliation, {2} Second author affiliation

*** Conflict of interest
The authors declare no conflict of interest
```

## Manuscript types

- preprints
- reports

