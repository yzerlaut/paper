<!---
#+Title: Presentation template
#+Subtitle: Assembling Inkscape slides with Latex-Beamer
#+Authors: First Author{1}, Second Author{1,2}*
#+Short_Title: Paper Template
#+Short_Authors: Author et al.
#+Affiliations: {1} My first affiliation, {2} Second author affiliation
#+with_titlepage: True
-->


# Outline

Outline:
%% \begin{multicols}{2}
\centering
\tableofcontents
%% \end{multicols}

# Motivation 

##  

\begin{itemize}
\item being able to use the layers of Inkscape to make animations
\item benefit from the pdf pages numbering 
\end{itemize}
   
# Methods 

## drawing slides in inkscape

[[slides/slide-template]]

## writing the presentation flow

[[slides/flow-writing]]

## slide animations

[[slides/animations]]
<!---
anim=[[1],
      [1,2],
      [1,2,3]]
-->

## compiling

Generate the figures for the presentation from the svgs with:

\begin{verbatim}

\$ python -m finalyz templates/presentation.md ----figures\_only

\end{verbatim}


\vspace{1cm}

Then compile the pdf document with:

\begin{verbatim}

\$ python -m finalyz templates/presentation.md

\end{verbatim}


# Results 

## presentation output

\centering

This presentation 


# Discussion

## to be done

In progress / to be done: 

\begin{itemize}
\item video integration
\item better integration of style
\end{itemize}

# thanks          

\centering

Thank you for your attention !

