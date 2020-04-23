<div><img src="https://github.com/yzerlaut/finalyz/raw/master/docs/report.png" alt="finalyz logo" width="65%" align="right" style="margin-left: 10px"></div>

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
- Bibliographic managment and export to different citation styles
- Benefit from the the Emacs editing capabilities (the txt template uses the Org-Mode syntax).

## Installation

Clone the repository and `source` the main script with:
```
git clone https://github.com/yzerlaut/finalyz
source finalyz/run.sh
```

## Use

- perform your quantitative analysis as store your results as `your_study_file.npz` (see the [documentation notebook](https://github.com/yzerlaut/finalyz/blob/master/docs/notebook.ipynb))
- draft your paper on a "txt" file (see the templates in the [template folder](https://github.com/yzerlaut/finalyz/tree/master/templates)
- compile it with:

```
finalyz you_paper.txt --study_file your_study_file.npz
```
(see the below section *Manuscript types* for a few shortcuts to specific journal formats, preprint types, ...)

## Include quantitative results 

We show here how to use cross-referencing extracted from an analysis file to report the results of the study. In this demo case (generated in the [documentation notebook](https://github.com/yzerlaut/finalyz/blob/master/docs/notebook.ipynb), the [study.npz](https://github.com/yzerlaut/finalyz/raw/master/study.npz) file contains both study parameters and analysis results:

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
The study was conducted over {study_duration}.
It contained {Nsample} of {Nobs} observations.
Signal was: {mean_value} $\pm$ {sem_value}.
Cross-correlation over observations was {cc_coef_over_obs_mean} $\pm$ {cc_coef_over_obs_mean} with minimum {cc_coef_over_obs_min} and maximum {cc_pval_over_obs_max}.
P-values of linear correlation spanned a range between pval={cc_pval_over_obs_min} and pval={cc_pval_over_obs_max}
```

are exported to:

> The study was conducted over 2 months. It contained 100 of 5 observations. Signal was: 1.605 ± 0.13. Cross- correlation over observations was 0.055 ± 0.055 with minimum -0.122 and maximum 0.856. P-values of linear correlation spanned a range between pval=0.026 and pval=0.856.

## Include references and choose citation style

Reference are included in the text by a plain text citation style:

```
A landwark study on visual cortex (Hubel and Wiesel, 1962), ...
```

The compiled citation will depend on the citation style used.
- For `finalyz your_paper.txt --citation_style text # default settings`, one gets:
> A landwark study on visual cortex (Hubel and Wiesel, 1962)

- For `finalyz your_paper.txt --citation_style number`, one gets:
> A landwark study on visual cortex [1]

- For `finalyz your_paper.txt --citation_style exponent_number`
> A landwark study on visual cortex<sup>1</sup>


All cited references should point to a bibtex entry in the `References` section, e.g.:
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

## Include equations
## Include figures

Make a dedicated `Figures` section and fill it with your caption (main caption in bold) and subcaption in normal text, e.g.:
```
* Figures

*** Main caption for the single-column figure: description of the protocol.
#+options : {'label':'Fig1', 'extent':'singlecolumn', 'file':'docs/fig1.png', 'page_position':'b!'}
Generate the figure with the file \texttt{surface\_plot.py} from the \texttt{graphs} module available at the following \href{https://bitbucket.org/yzerlaut/graphs/src/master/}{[link]}. Lorem ipsum dolor sit amet, consectetuer adipisc- ing elit. Etiam lobortis facilisis sem. Nullam nec mi et neque pharetra sollicitudin. We added an optional horizontal rule at the bottom.
```

```
[[Figure {protocol-description} around here]]
```


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

