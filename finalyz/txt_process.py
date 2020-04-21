"""
We start from a txt file compatible with the org-mode format and want to export it to a tex file
"""
import os
import numpy as np

from tex_templates import *
from functions import *
from bib_process import process_references


INFORMATION_KEYS = ['Title', 'Short_Title',
                    'Authors', 'Short_Authors',
                    'Affiliations', 'Correspondence',
                    'Keywords', 'Conflict_of_interest',
                    'Acknowledgements', 'Funding']



PAPER = {'text':'', # full text
         'Preamble':'',
         'Abstract':'',
         'Significance':'','Key Points':'',
         'Main Text':'',
         'Introduction':'','Methods':'','Results':'','Discussion':'',
         'Figures':'', 'Tables':'',
         'Supplementary':'', 'Supplementary Figures':'', 'Supplementary Tables':'',
         'References':'',
         'refs':{},\
         # figures/tables/eqs elements
         'FIGS':[], 'TABLES':[],
         'SUPP_FIGS':[], 'SUPP_TABLES':[], 'EQS':[]}
# adding informations section
for key in INFORMATION_KEYS:
    PAPER[key] = ''


def choose_export_style(args):

    PAPER['TEX'] = BASIC_TEX
    args.manuscript_submission, args.figures_at_the_end, args.cross_ref = False, False, True
    PAPER['order'] = ['Introduction', 'Results', 'Discussion', 'Methods'] # default
    if args.figures_only:
        PAPER['TEX'] = FIGURES_ONLY
    elif (args.journal=='preprint') or args.report:
        PAPER['TEX'] = TEX
    elif (args.journal=='Nature'):
        args.citation_style = 'number_exponents'
    elif (args.journal=='PLoS'):
        args.citation_style = 'number'
    elif (args.journal=='JNeurosci'):
        PAPER['order'] = ['Introduction', 'Methods', 'Results', 'Discussion']
        args.manuscript_submission = True
        PAPER['TEX'] = JNEUROSCI
    elif (args.journal=='JPhysiol'):
        PAPER['order'] = ['Introduction', 'Methods', 'Results', 'Discussion']
        args.manuscript_submission = True
        PAPER['TEX'] = JPHYSIOL
        
    if args.with_doc_export:
        args.cross_ref = False
        args.manuscript_submission = True
        args.figures_at_the_end = True
        PAPER['TEX'] = BASIC_TEX
    # # adding the draft option to debug
    if args.debug_draft or args.draft:
        PAPER['TEX'] = PAPER['TEX'].replace('\\begin{{document}}', '\hypersetup{{draft}}\n\\begin{{document}}')
        PAPER['TEX'] = PAPER['TEX'].replace(']{{article}}', ',draft]{{article}}')
        
        


def process_manuscript(args):

    choose_export_style(args)
    
    # extracting the full text from the manuscript
    with open(args.filename) as f:
        content = f.readlines()
        full_text = ''
        for c in content:
            full_text+=c

    # organizing the text, secion by section
    SECTIONS = full_text.split('\n* ') # separator for the start of a given section in org-mode
    PAPER['Preamble'] = SECTIONS[0] # text above the section is the preamble
    for key in ['Main Text',
                'Abstract', 'Significance', 'Key Points',
                'Introduction', 'Methods', 'Results', 'Discussion',
                'References',
                'Figures', 'Tables',
                'Supplementary',
                # 'Supplementary Text', 'Supplementary Figures', 'Supplementary Tables',
                'Informations']:
        for i in range(len(SECTIONS)):
            if len(SECTIONS[i][:40].split(key))>1:
                PAPER[key] = SECTIONS[i]

    #######################
    ## PRE-PROCESS INFOS
    process_preamble_and_informations(PAPER, args, INFORMATION_KEYS)

    if len(PAPER['Figures'])>10:
        process_figures(PAPER, args)
    
    if len(PAPER['Supplementary Figures'])>10:
        process_figures(PAPER, args, supplementary=True)

    if len(PAPER['Tables'])>10:
        process_tables(PAPER, args)

    if len(PAPER['Main Text'])>10:
        process_main_text(PAPER, args)

    # manuscript organization: assemble the text from the sections
    process_section_titles(PAPER, args)

    ##########################
    ## ASSEMBLE MANUSCRIPT
    PAPER['text'] = ''
    
    if not args.figures_only:
        
        if len(PAPER['Key Points'])>10:
            insert_key_points(PAPER, args)
        if len(PAPER['Abstract'])>10:
            insert_abstract(PAPER, args)
        if len(PAPER['Significance'])>10:
            insert_significance(PAPER, args)

        if args.report:
            PAPER['text'] += PAPER['Main Text']
        else:
            for key in PAPER['order']:
                PAPER['text'] += PAPER[key]
                
        process_subsection_titles(PAPER, args)

        # first including the latex figures
        replace_text_indication_with_latex_fig(PAPER, args)
        replace_text_indication_with_latex_table(PAPER, args)
        
    else:
        add_figures_and_tables_at_the_end(PAPER, args)
        
    # # supplementary at the end
    if args.with_supplementary:
        insert_supplementary(PAPER, args)
    
    # then cross-referencing
    include_figure_cross_referencing(PAPER, args)
    include_table_cross_referencing(PAPER, args)

    if not args.figures_only:
        process_references(PAPER, args)
        process_equations(PAPER, args)

    if os.path.isfile(args.study_file):
        print('\n using "%s" as the "study-file" !' % args.study_file)
        for key, val in dict(np.load(args.study_file)).items():
            PAPER['text'] = PAPER['text'].replace('{'+key+'}', str(val))
    else:
        print('No analysis file used ...')
        print('"%s" not found' % args.study_file)

    final_manuscript_analysis(PAPER, args)

    os.system('if [ -d "tex/" ]; then echo ""; else mkdir tex/; fi;')
    with open(args.tex_file, 'w') as f:
        final_text = PAPER['TEX'].format(**PAPER)
        f.write(final_text)

    return PAPER

    
    
# if __name__=='__main__':

#     import argparse
#     parser=argparse.ArgumentParser(description=
#      """ 
#      A script to export simple txt files manuscripts
#      """
#     ,formatter_class=argparse.RawTextHelpFormatter)
    
#     parser.add_argument("--filename", '-f', help="filename",type=str, default='paper.txt')
#     parser.add_argument('-j', "--journal", help="journal type", type=str, default='preprint')
#     parser.add_argument('-sf', "--study_file", help="analysis filename", type=str, default='analysis.npz')
#     parser.add_argument("-r", "--report", help="", action="store_true")
#     parser.add_argument("-fo", "--figures_only", help="", action="store_true")
#     parser.add_argument("-fk", "--figure_key", help="Type of references to figures: either 'Figure' of 'Fig.' ", default='Fig.')
#     parser.add_argument("-ek", "--equation_key", help="Type of references to equations: either 'Equation' of 'Eq.' ", default='Eq.')
#     parser.add_argument("-tk", "--table_key", help="Type of references to tables: either 'Table' of 'Tab.' ", default='Table')
#     parser.add_argument("-p", "--print", help="print the tex file", action="store_true")
#     parser.add_argument("-js", "--journal_submission", help="format for submitting to journals", action="store_true")
#     parser.add_argument("--citation_style", help="number / text ", type=str, default='text')
#     parser.add_argument("--reference_style", help="APA / [...] ", type=str, default='APA')
#     parser.add_argument("-wdoc", "--with_doc_export", help="with Ms-Word export", action="store_true")
#     parser.add_argument("--debug", help="", action="store_true")
#     parser.add_argument("--debug_draft", help="", action="store_true")
#     parser.add_argument("--draft", help="", action="store_true")
    
#     args = parser.parse_args()

#     args.tex_file = os.path.join('tex', os.path.basename(args.filename).replace('.txt', '.tex'))
#     args.pdf_file = os.path.join('tex', os.path.basename(args.filename).replace('.txt', '.pdf'))
    
#     process_manuscript(args)
    
#     if args.with_doc_export:
#         export_to_docx(args)
#     else:
#         export_to_pdf(args)
