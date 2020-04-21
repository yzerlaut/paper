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

## User guide

Work on your "txt" file (see the templates in the [template folder](https://github.com/yzerlaut/finalyz/tree/master/templates) 




## Manual

### Manuscript types

- preprints
- reports


### Manuscript informations

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

### References
