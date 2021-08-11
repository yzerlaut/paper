"""
We start from a txt file compatible with the org-mode format and want to export it to a tex file
"""
import os
import numpy as np

from tex_templates import BEAMER_CLASS, BEAMER_TEMPLATE
from functions import *

INFORMATION_KEYS = ['Title', 'Subtitle', 'Short_Title',
                    'Authors', 'Short_Authors', 'Affiliations']

PRES = {'text':'', # full text
        'Preamble':'',
        'Informations':'',
        'Affiliations':'',
        'Correspondence':''}

# adding informations section
for key in INFORMATION_KEYS:
    PRES[key] = ''

def add_images_on_slide(subsection, PRES, base_dir):

    location = subsection.split(']]')[0].split('[[')[1]
    filename = location.split(os.path.sep)[-1]
    
    PRES['text'] += '\\begin{frame}{}\n'
    files = [f for f in os.listdir(os.path.join(base_dir,'slides', 'pngs')) if (filename in f)]
    for i, f in enumerate(files):
        PRES['text'] += '\only<%i>{\n' % (i+1)
        PRES['text'] += '\\vspace*{-1mm} \hspace*{-11mm}'
        PRES['text'] += '\includegraphics[width=\paperwidth]{%s}' % os.path.join(base_dir,'slides', 'pngs', f)
        PRES['text'] += '}\n'
        
    PRES['text'] += '%s \n' % filename
    PRES['text'] += '\\end{frame}{}\n\n'
    print(location)

def process_presentation(args):

    # extracting the full text from the manuscript
    with open(args.filename) as f:
        content = f.readlines()
        full_text = ''
        for c in content:
            full_text+=c
    # organizing the text, secion by section
    SECTIONS = full_text.split('\n* ') # separator for the start of a given section in org-mode

    ####### PREAMBLE ##########
    PRES['Preamble'] = SECTIONS[0] # text above the section is the preamble

    process_preamble_and_informations(PRES, args, INFORMATION_KEYS)

    istart=1
    if ('Table of content' in SECTIONS[1]) or ('Outline' in SECTIONS[1]):
        PRES['text'] += '\\begin{frame}{}\n'
        for l in SECTIONS[1].split('\n')[1:]:
            PRES['text'] += l+'\n'
        PRES['text'] += '\\end{frame}{}\n\n'
        istart=2

    for isec in range(istart, len(SECTIONS)):
        section = SECTIONS[isec].split('\n')[0]
        if 'thanks' in section:
            PRES['text'] += '\\section*{\\quad}\n'
            text = SECTIONS[isec].split('\n')[1:]
            if '[[' in text:
                add_images_on_slide(text[1], PRES, os.path.dirname(args.filename))
            else: # we just paste the content into frames
                PRES['text'] += '\\begin{frame}{}\n'
                for l in text:
                    PRES['text'] += l+'\n'
                PRES['text'] += '\\end{frame}{}\n\n'
        else:
            PRES['text'] += '\\section{%s}\n' % section
        
        for subsection in SECTIONS[isec].split('\n** ')[1:]:
            PRES['text'] += '\\subsection{%s}\n' % subsection.split('\n')[0]
            if '[[' in subsection:
                add_images_on_slide(subsection, PRES, os.path.dirname(args.filename))
            else: # we just paste the content into frames
                PRES['text'] += '\\begin{frame}{}\n'
                for l in subsection.split('\n')[1:]:
                    PRES['text'] += l+'\n'
                PRES['text'] += '\\end{frame}{}\n\n'
                
    # # manuscript organization: assemble the text from the sections


    # ##########################
    # ## ASSEMBLE MANUSCRIPT
    # PAPER['text'] = ''
    
    # if not args.figures_only:
        
    #     if len(PAPER['Key Points'])>10:
    #         insert_key_points(PAPER, args)
    #     if len(PAPER['Abstract'])>10:
    #         insert_abstract(PAPER, args)
    #     if len(PAPER['Significance'])>10:
    #         insert_significance(PAPER, args)

    #     if args.report:
    #         PAPER['text'] += PAPER['Main Text']
    #     else:
    #         for key in PAPER['order']:
    #             PAPER['text'] += PAPER[key]
                
    #     process_subsection_titles(PAPER, args)

    #     # first including the latex figures
    #     replace_text_indication_with_latex_fig(PAPER, args)
    #     replace_text_indication_with_latex_table(PAPER, args)
        
    # else:
    #     add_figures_and_tables_at_the_end(PAPER, args)

    # # then cross-referencing
    # include_figure_cross_referencing(PAPER, args)
    # if args.with_supplementary:
    #     include_figure_cross_referencing(PAPER, args, supplementary=True)
    # include_table_cross_referencing(PAPER, args)

    # if not args.figures_only:
    #     process_references(PAPER, args)
    #     process_equations(PAPER, args)

    # if args.insert_informations_at_the_end:
    #     insert_informations_at_the_end(PAPER, args)
        
    # # # supplementary at the end
    # if args.with_supplementary:
    #     insert_supplementary(PAPER, args)
    #     include_figure_cross_referencing(PAPER, args,
    #                                      supplementary=True)
        
    # if os.path.isfile(args.study_file):
    #     print('\n using "%s" as the "study-file" !' % args.study_file)
    #     try:
    #         study = np.load(args.study_file, allow_pickle=True).item()
    #         for key, val in study.items():
    #             PAPER['text'] = PAPER['text'].replace('{'+key+'}', str(val))
    #     except BaseException as be:
    #         print(be)
    #         print('\n ---> Problem with "%s" !' % args.study_file)
    # else:
    #     print('No analysis file used ...')
    #     print('"%s" not found' % args.study_file)

    # final_manuscript_analysis(PAPER, args)

    # if not os.path.isdir('tex'):
    #     os.mkdir('tex')
        
    # with open(args.tex_file, 'w') as f:
    #     final_text = PAPER['TEX'].format(**PAPER)
    #     f.write(final_text)

    return PRES


if __name__=='__main__':

    import argparse
    parser=argparse.ArgumentParser(description=
     """ 
     A script to export simple txt files manuscripts
     """
    ,formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument('-f', "--filename", help="filename",type=str, default='presentation.txt')
    # parser.add_argument("-wdoc", "--with_doc_export", help="with Ms-Word export", action="store_true")
    parser.add_argument("--debug", help="", action="store_true")
    parser.add_argument("--debug_draft", help="", action="store_true")
    # parser.add_argument("--draft", help="", action="store_true")
    
    args = parser.parse_args()

    PRES = process_presentation(args)

    os.system('if [ -d "tex/" ]; then echo ""; else mkdir tex/; fi;')

    with open('tex/simple.cls', 'w') as f:
        txt = BEAMER_CLASS.format(**PRES)
        f.write(str(txt))

    with open('tex/pres.tex', 'w') as f:
        txt = BEAMER_TEMPLATE.format(**PRES)
        f.write(str(txt))

    args.tex_file = 'tex/pres.tex'
    args.pdf_file = 'tex/pres.pdf'

    export_to_pdf(args)
    
    
    
