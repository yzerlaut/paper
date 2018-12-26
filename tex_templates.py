TEX = \
"""
\\documentclass[8pt, a4paper, twocolumn, twoside, colorlinks]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{longtable, float, wrapfig, rotating, graphicx, multirow}}
\\usepackage{{amsmath, textcomp, marvosym, wasysym, amssymb, hyperref, wrapfig}}
\\tolerance=1000
\\setcounter{{tocdepth}}{{5}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{lmodern, microtype}} % Slightly tweak font spacing for aesthetics
\\usepackage{{geometry}}
\\geometry{{a4paper,total={{210mm,297mm}}, left=15mm, right=15mm, top=20mm, bottom=20mm, bindingoffset=0mm, columnsep=.5cm}}
\\usepackage[labelfont=bf,labelsep=period,font=small]{{caption}}
\\captionsetup[table]{{position=bottom}}
\\newcommand\\blfootnote[1]{{  \\begingroup  \\renewcommand\\thefootnote{{}}\\footnote{{#1}}  \\addtocounter{{footnote}}{{-1}}  \\endgroup}}
\\newcommand\\up[1]{{\\textsuperscript{{#1}}}}
\\newcommand\\mailto[1]{{\\href{{mailto:#1}}{{#1}}}}
\\def\\dag{{$\\dagger$}}
\\def\\shortdate{{\\today}}
\\hypersetup{{allcolors = [rgb]{{0.1,0.1,0.6}} }} % to have all the hyperlinks in 1 color
% \\def\\todo#1{{\\marginpar{{\\colorbox{{red}}{{TODO}}}}{{(TODO: \\textit{{#1}})}}}}
% \\def\\todo#1{{\\colorbox{{red}}{{TODO}}{{(\\underline{{#1}})}}}}
% \\def\\note#1{{\\colorbox{{green}}{{\\underline{{#1}}}}}}
\\def\\TODO#1{{\\colorbox{{red}}{{TODO: \\underline{{#1}}}}{{}}}}
\\def\\NOTE#1{{\\colorbox{{green}}{{\\underline{{#1}}}}{{}}}}
\\usepackage{{fancyhdr}} % Headers and footers
\\pagestyle{{fancy}} % All pages have headers and footers
\\fancyhead{{}} % Blank out the default header
\\fancyfoot{{}} % Blank out the default footer
\\fancyhead[C]{{\\footnotesize \\shorttitle \\quad $\\bullet$ \\quad \\shortauthor \\quad $\\bullet$ \\quad \\shortdate \\normalsize }}
\\fancyfoot[C]{{\\thepage}} % Custom footer text
\\makeatletter
\\usepackage{{titlesec}} % Allows customization of titles
\\def\\@maketitle{{  \\newpage  \\null  \\vspace{{-10mm}}   \\begin{{center}}  \\let \\footnote \\thanks    {{\\Large \\textbf{{\\@title}} \\par}}    \\vskip 1.2em    {{\\large      \\lineskip .5em      \\begin{{tabular}}[t]{{c}}        \\scshape      \\normalsize        \\@author      \\end{{tabular}}\\par}}   \\vskip .6em   {{ \\@date}}  \\end{{center}}  \\par  \\vskip 0.1em}}
\\makeatother

\\newcommand{{\\beginsupplement}}{{
     \\setcounter{{table}}{{0}}
     \\renewcommand{{\\thetable}}{{S\\arabic{{table}}}}
     \\setcounter{{figure}}{{0}}
     \\renewcommand{{\\thefigure}}{{S\\arabic{{figure}}}}
}}


\\author{{ {authors} }}
\\title{{ {title} }}
\\def\\shorttitle{{ {short_title} }}
\\def\\shortauthor{{ {short_authors} }}
\\date{{ \\today }}


\\begin{{document}}

\\maketitle

\\blfootnote{{  {affiliations} \, }}
\\blfootnote{{  *Correspondence: {correspondence} }}

{text}

\\end{{document}}
"""

JNEUROSCI = \
"""
\\documentclass[9pt, a4paper, colorlinks]{{article}}
\\linespread{{1.5}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc, fixltx2e, graphicx, longtable, float, wrapfig, rotating, graphicx, multirow}}
\\usepackage{{amsmath, textcomp, marvosym, wasysym, amssymb, lmodern, setspace}}
\\usepackage{{hyperref}}
\\hypersetup{{allcolors = [rgb]{{0.1,0.1,0.6}} }} % to have all the hyperlinks in 1 color
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{geometry}}
\\geometry{{a4paper,total={{210mm,297mm}}, left=15mm, right=15mm, top=20mm, bottom=20mm, bindingoffset=0mm}}
\\usepackage{{lineno}}
\\title{{ {title} }}
\\author{{ {authors}  }}
\\date{{ \\vspace{{ 2cm }} }}

\\begin{{document}}
\\maketitle

\\underline{{\\textsc{{Affiliations:}}}} {affiliations} \\newline \\vspace{{ 1mm }}

\\underline{{\\textsc{{Abbreviated Title:}}}} {short_title} \\newline \\vspace{{ 1mm }}

\\underline{{\\textsc{{Correspondence:}}}} {Correspondence} \\newline \\vspace{{ 1mm }}

\\underline{{\\textsc{{Keywords:}}}} {Keywords} \\newline \\vspace{{ 1mm }}

\\underline{{\\textsc{{Number of Figures:}}}} {Num_of_Figures} \\newline \\vspace{{ 1mm }}

\\underline{{\\textsc{{Number of Tables:}}}}  {Num_of_Tables} \\newline \\vspace{{ 1mm }}

\\underline{{\\textsc{{Number of Words:}}}} Abstract ({Num_Words_of_Abstract} words), Introduction ({Num_Words_of_Introduction} words), Discussion ({Num_Words_of_Discussion} words) \\newline \\vspace{{ 1mm }}

\\underline{{\\textsc{{Conflict of Interest:}}}} {conflict_of_interest} \\newline \\vspace{{ 1mm }}

\\underline{{\\textsc{{Acknowledgements:}}}} {Acknowledgements} {Funding} \\newline \\vspace{{ 1mm }}

\\newpage 
\\linenumbers

\\subsection*{{Abstract}}
\\bfseries
{Abstract}
\\normalfont

\\subsection*{{Significance Statement}}
{Significance}

{text}
\\end{{document}}
"""

BASIC_TEX = \
"""
\\documentclass[9pt, a4paper, colorlinks]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc, fixltx2e, graphicx, longtable, float, wrapfig, rotating, graphicx}}
\\usepackage{{amsmath, textcomp, marvosym, wasysym, amssymb, lmodern}}
\\usepackage{{hyperref}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{geometry}}
\\geometry{{a4paper,total={{210mm,297mm}}, left=15mm, right=15mm, top=20mm, bottom=20mm, bindingoffset=0mm, columnsep=.5cm}}\\geometry{{a4paper,total={{210mm,297mm}}, left=15mm, right=15mm, top=20mm, bottom=20mm, bindingoffset=0mm, columnsep=.5cm}}
\\author{{ {authors} }}
\\title{{ {title} }}
\\date{{ \\today }}
\\newcommand{{\\beginsupplement}}{{
     \\setcounter{{table}}{{0}}
     \\renewcommand{{\\thetable}}{{S\\arabic{{table}}}}
     \\setcounter{{figure}}{{0}}
     \\renewcommand{{\\thefigure}}{{S\\arabic{{figure}}}}
}}
\\begin{{document}}
\\maketitle
{text}
\\end{{document}}
"""

FIGURES_ONLY = \
"""
\\documentclass[9pt, a4paper]{{article}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[labelfont=bf,labelsep=period,font=small]{{caption}}
\\usepackage[T1]{{fontenc, fixltx2e, graphicx, longtable, float, wrapfig, rotating, graphicx}}
\\usepackage{{amsmath, textcomp, marvosym, wasysym, amssymb, lmodern}}
\\usepackage[utf8]{{inputenc}}
\\usepackage[T1]{{fontenc}}
\\usepackage{{geometry}}
\\geometry{{a4paper,total={{210mm,297mm}}, left=15mm, right=15mm, top=20mm, bottom=20mm, bindingoffset=0mm, columnsep=.5cm}}\\geometry{{a4paper,total={{210mm,297mm}}, left=15mm, right=15mm, top=20mm, bottom=20mm, bindingoffset=0mm, columnsep=.5cm}}
\\begin{{document}}
{text}
\\end{{document}}
"""
