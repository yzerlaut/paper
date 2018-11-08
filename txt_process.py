"""
We start from a txt file compatible with the org-mode format and want to export it to a tex file
"""
import os
import string
import numpy as np

NEW = []
PAPER = {'text':'',
         'Preamble':'',
         'Significance':'','Key Points':'', 'Abstract':'',
         'Introduction':'','Methods':'','Results':'','Discussion':'',
         'Figures':'', 'Tables':'', 'Supplementary':'',
         'References':'',
         'refs':{},\
         'authors':'', 'short_authors':'',
         'title':'', 'short_title':'',
         'affiliations':'', 'correspondence':'',
         'FIGS':[], 'TABLES':[], 'EQS':[]}

TEX = \
"""
%\\documentclass[8pt, a4paper, twocolumn, twoside, colorlinks]{{article}}
\\documentclass[9pt, a4paper, colorlinks]{{article}}
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
\\def\\todo#1{{\\colorbox{{red}}{{TODO: \\underline{{#1}}}}{{}}}}
\\def\\note#1{{\\colorbox{{green}}{{\\underline{{#1}}}}{{}}}}
\\usepackage{{fancyhdr}} % Headers and footers
\\pagestyle{{fancy}} % All pages have headers and footers
\\fancyhead{{}} % Blank out the default header
\\fancyfoot{{}} % Blank out the default footer
\\fancyhead[C]{{\\footnotesize \\shorttitle \\quad $\\bullet$ \\quad \\shortauthor \\quad $\\bullet$ \\quad \\shortdate \\normalsize }}
\\fancyfoot[C]{{\\thepage}} % Custom footer text
\\makeatletter
\\usepackage{{titlesec}} % Allows customization of titles
\\def\\@maketitle{{  \\newpage  \\null  \\vspace{{-10mm}}   \\begin{{center}}  \\let \\footnote \\thanks    {{\\Large \\textbf{{\\@title}} \\par}}    \\vskip 1.2em    {{\\large      \\lineskip .5em      \\begin{{tabular}}[t]{{c}}        \\scshape      \\normalsize        \\@author      \\end{{tabular}}\\par}}   \\vskip .6em   {{ \\@date}}  \\end{{center}}  \\par  \\vskip 1em}}
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

\\blfootnote{{ 
 {affiliations} \, 
}}

\\blfootnote{{ 
*Correspondence: 
{correspondence} 
}}


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

from functions import *

def choose_style_from_journal(args):

    if (args.journal=='Nature') or (args.journal=='PloS'):
        args.citation_style = 'number'
        

def process_manuscript(args):

    choose_style_from_journal(args)
    
    Supplementary_Flag = False # for Figures
    
    # extracting the full text from the manuscript
    with open(args.filename) as f:
        content = f.readlines()
        full_text = ''
        for c in content:
            full_text+=c

    # organizing the text, secion by section
    SECTIONS = full_text.split('\n* ') # separator for the start of a given section in org-mode
    PAPER['Preamble'] = SECTIONS[0] # text above the section is the preamble
    for key in ['Abstract', 'Introduction', 'Methods', 'Results',\
                'Supplementary','References', 'Figures', 'Tables',\
                'Significance', 'Discussion', 'Key Points']:
        for i in range(len(SECTIONS)):
            if len(SECTIONS[i][:15].split(key))>1:
                PAPER[key] = SECTIONS[i]

    # process figures
    transform_preamble_into_title_props(PAPER, args)
    
    # process figures
    process_figures(PAPER, args)
    
    # manuscript organization: assemble the text from the sections
    process_section_titles(PAPER, args)
    assemble_text(PAPER, args)
    
    replace_text_indication_with_latex_fig(PAPER, args)

    process_references(PAPER, args)
    

    with open(args.filename.replace('.txt', '.tex'), 'w') as f:
        final_text = TEX.format(**PAPER)
        f.write(TEX.format(**PAPER))
        f.write(final_text)
                
def export_to_pdf(args):
    os.system('if [ -d "tex/" ]; then echo ""; else mkdir tex/; fi;')
    tex_file = args.filename.replace('.txt', '.tex')
    pdf_file = args.filename.replace('.txt', '.pdf')
    os.system('mv '+tex_file+' tex/'+tex_file)
    os.system('pdflatex -shell-escape -interaction=nonstopmode -output-directory=tex/ tex/'+tex_file+' > tex/compil_output')
    os.system('mv tex/'+pdf_file+' '+pdf_file)

def export_to_docx(args):
    """
    needs pandoc
    """
    os.system('if [ -d "tex/" ]; then echo ""; else mkdir tex/; fi;')
    tex_file = args.filename.replace('.txt', '.tex')
    docx_file = args.filename.replace('.txt', '.docx')
    # os.system('mv '+tex_file+' tex/'+tex_file)
    os.system('pandoc '+tex_file+' -o '+docx_file)

    
    
if __name__=='__main__':

    import argparse
    parser=argparse.ArgumentParser(description=
     """ 
     A script to export simple txt files manuscripts
     """
    ,formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument("--filename", '-f', help="filename",type=str, default='paper.txt')
    parser.add_argument('-j', "--journal", help="journal type", type=str, default='preprint')
    parser.add_argument('-af', "--analysis_output_file", help="analysis filename", type=str, default='paper.npz')
    parser.add_argument("-r", "--report", help="", action="store_true")
    parser.add_argument("-fo", "--figures_only", help="", action="store_true")
    parser.add_argument("-fk", "--figure_key", help="Type of references to figures: either 'Figure' of 'Fig.' ", default='Fig.')
    parser.add_argument("-ek", "--equation_key", help="Type of references to equations: either 'Equation' of 'Eq.' ", default='Eq.')
    parser.add_argument("-tk", "--table_key", help="Type of references to tables: either 'Table' of 'Tab.' ", default='Table')
    parser.add_argument("-p", "--print", help="print the tex file", action="store_true")
    parser.add_argument("-js", "--journal_submission", help="format for submitting to journals", action="store_true")
    parser.add_argument("--citation_style", help="number / text ", type=str, default='text')
    parser.add_argument("--reference_style", help="APA / [...] ", type=str, default='APA')
    parser.add_argument("-wdoc", "--with_doc_export", help="with Ms-Word export", action="store_true")
    
    args = parser.parse_args()

    process_manuscript(args)
    
    if args.with_doc_export:
        export_to_docx(args)
    else:
        export_to_pdf(args)
    
