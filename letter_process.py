"""
We start from a txt file compatible with the org-mode format and want to export it to a tex file
"""
import os
import numpy as np

from tex_templates import *
from functions import *
from txt_process import export_to_pdf, export_to_docx

NEW = []
LETTER = {'text':'',
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


def process_letter(args):

    # extracting the full text from the manuscript
    with open(args.filename) as f:
        content = f.readlines()
        full_text = ''
        for c in content:
            full_text+=c

    LETTER = {'TEX':TEX_LETTER}
    with open(args.filename.replace('.txt', '.tex'), 'w') as f:
        final_text = LETTER['TEX'].format(**LETTER)
        f.write(final_text)

        
if __name__=='__main__':

    import argparse
    parser=argparse.ArgumentParser(description=
     """ 
     A script to export simple txt files manuscripts
     """
    ,formatter_class=argparse.RawTextHelpFormatter)
    
    parser.add_argument("--filename", '-f', help="filename",type=str, default='letter.txt')
    parser.add_argument("-wdoc", "--with_doc_export", help="with Ms-Word export", action="store_true")
    parser.add_argument("--debug", help="", action="store_true")
    parser.add_argument("--debug_draft", help="", action="store_true")
    parser.add_argument("--draft", help="", action="store_true")
    
    args = parser.parse_args()

    process_letter(args)
    
    if args.with_doc_export:
        export_to_docx(args)
    else:
        export_to_pdf(args)
