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
                    'Data_availability',
                    'Acknowledgements', 'Funding']



PAPER = {'text':'', # full text
         'Preamble':'',
         'Abstract':'',
         'Significance':'','Key Points':'',
         'Main Text':'',
         'Introduction':'','Methods':'','Results':'','Discussion':'',
         'Figures':'', 'Tables':'',
         'Supplementary':'',
         # 'Supplementary Figures':'', 'Supplementary Tables':'',
         'References':'',
         'Informations':'',
         'Other':'', # this shouldn't be exported
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
                'Other',
                'Informations']:
        for i in range(len(SECTIONS)):
            if (len(SECTIONS[i][:40].split(key))>1) and (key=='Supplementary') and args.with_supplementary:
                SUBSECTIONS = SECTIONS[i].split('\n** ') # separator for the start of a given section in org-mode
                for skey in ['Supplementary Text', 'Supplementary Figures', 'Supplementary Tables']:
                    for j in range(len(SUBSECTIONS)):
                        if len(SUBSECTIONS[j][:40].split(skey))>1:
                            PAPER[skey] = SUBSECTIONS[j]
            elif len(SECTIONS[i][:40].split(key))>1:
                PAPER[key] = SECTIONS[i]

    #######################
    ## PRE-PROCESS INFOS
    process_preamble_and_informations(PAPER, args, INFORMATION_KEYS)

    if len(PAPER['Figures'])>10:
        process_figures(PAPER, args)
        
    if args.with_supplementary and ('Supplementary Figures' in PAPER):
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

    # then cross-referencing
    include_figure_cross_referencing(PAPER, args)
    if args.with_supplementary:
        include_figure_cross_referencing(PAPER, args, supplementary=True)
    include_table_cross_referencing(PAPER, args)

    if not args.figures_only:
        process_references(PAPER, args)
        process_equations(PAPER, args)

    if args.insert_informations_at_the_end:
        insert_informations_at_the_end(PAPER, args)
        
    # # supplementary at the end
    if args.with_supplementary:
        insert_supplementary(PAPER, args)
        include_figure_cross_referencing(PAPER, args,
                                         supplementary=True)
        
    if os.path.isfile(args.study_file):
        print('\n using "%s" as the "study-file" !' % args.study_file)
        try:
            study = np.load(args.study_file, allow_pickle=True).item()
            for key, val in study.items():
                PAPER['text'] = PAPER['text'].replace('{'+key+'}', str(val))
        except BaseException as be:
            print(be)
            print('\n ---> Problem with "%s" !' % args.study_file)
    else:
        print('No analysis file used ...')
        print('"%s" not found' % args.study_file)

    final_manuscript_analysis(PAPER, args)

    if not os.path.isdir('tex'):
        os.mkdir('tex')
        
    with open(args.tex_file, 'w') as f:
        final_text = PAPER['TEX'].format(**PAPER)
        f.write(final_text)

    return PAPER
