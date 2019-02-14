"""
We start from a txt file compatible with the org-mode format and want to export it to a tex file
"""
import os
import numpy as np

from tex_templates import *
from functions import *

NEW = []
PAPER = {'text':'',
         'Preamble':'',
         'Abstract':'',
         'Significance':'','Key Points':'','Keywords':'', 'Acknowledgements':'', 'Funding':'',
         'Introduction':'','Methods':'','Results':'','Discussion':'',
         'Figures':'', 'Tables':'', 'Supplementary':'',
         'References':'',
         'refs':{},\
         'authors':'', 'short_authors':'',
         'title':'', 'short_title':'',
         'affiliations':'', 'correspondence':'',
         'FIGS':[], 'TABLES':[], 'EQS':[]}


def choose_style_from_journal(args):

    PAPER['TEX'] = BASIC_TEX
    args.manuscript_submission, args.figures_at_the_end, args.cross_ref = False, False, True
    PAPER['order'] = ['Introduction', 'Results', 'Discussion', 'Methods'] # default
    if args.figures_only:
        PAPER['TEX'] = FIGURES_ONLY
    elif (args.journal=='preprint'):
        PAPER['TEX'] = TEX
    elif (args.journal=='Nature'):
        args.citation_style = 'number'
    elif (args.journal=='PLoS'):
        args.citation_style = 'number'
    elif (args.journal=='JNeurosci'):
        PAPER['order'] = ['Introduction', 'Methods', 'Results', 'Discussion']
        args.manuscript_submission = True
        PAPER['TEX'] = JNEUROSCI
    if args.with_doc_export:
        args.cross_ref = False
        args.manuscript_submission = True
        args.figures_at_the_end = True
        PAPER['TEX'] = BASIC_TEX


def process_manuscript(args):

    choose_style_from_journal(args)
    
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
    process_tables(PAPER, args)
    
    # manuscript organization: assemble the text from the sections
    process_section_titles(PAPER, args)

    assemble_text(PAPER, args)

    # first including the latex figures
    if not args.figures_at_the_end:
        replace_text_indication_with_latex_fig(PAPER, args)
        replace_text_indication_with_latex_table(PAPER, args)
    else:
        add_figures_and_tables_at_the_end(PAPER, args)
        
    # then cross-referencing
    include_figure_cross_referencing(PAPER, args)
    include_table_cross_referencing(PAPER, args)

    if not args.figures_only:
        process_references(PAPER, args)
        process_equations(PAPER, args)

    if os.path.isfile(args.analysis_output_file):
        print('using "'+args.analysis_output_file+'" for analysis data')
        for key, val in dict(np.load(args.analysis_output_file)).items():
            PAPER['text'] = PAPER['text'].replace('{'+key+'}', str(val))
    else:
        print('No analysis file used ...')
        print('"'+args.analysis_output_file+'" not found')

    final_manuscript_analysis(PAPER, args)
        
    with open(args.filename.replace('.txt', '.tex'), 'w') as f:
        final_text = PAPER['TEX'].format(**PAPER)
        f.write(final_text)

        
def export_to_pdf(args):
    os.system('if [ -d "tex/" ]; then echo ""; else mkdir tex/; fi;')
    tex_file = args.filename.replace('.txt', '.tex')
    pdf_file = args.filename.replace('.txt', '.pdf')
    os.system('mv '+tex_file+' tex/'+tex_file)
    if args.debug:
        os.system('pdflatex -output-directory=tex/ tex/'+tex_file)
    else:
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
    parser.add_argument('-af', "--analysis_output_file", help="analysis filename", type=str, default='analysis.npz')
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
    parser.add_argument("--debug", help="", action="store_true")
    
    args = parser.parse_args()

    process_manuscript(args)
    
    if args.with_doc_export:
        export_to_docx(args)
    else:
        export_to_pdf(args)
    
