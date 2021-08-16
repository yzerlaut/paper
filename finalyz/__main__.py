import argparse, os

from . import paper, presentation, letter, functions, biblio

parser=argparse.ArgumentParser(description=
 """ 

 Interface to the finalyz program. The script process manuscript and bibliography files.

 """
,formatter_class=argparse.RawTextHelpFormatter)


# filename
parser.add_argument("filename", help="filename (either a '.txt' or a '.bib' file)", type=str)
parser.add_argument("processing", help="either:\n       'bibliography/bib', 'paper', 'report', 'presentation' ", type=str)

# type of manuscript
parser.add_argument('-j', "--journal",
                    help="journal type for 'paper' processing", type=str, default='preprint')
parser.add_argument('-sf', "--study_file",
                    help="study parameters and analysis ouput", type=str, default='study.npy')
parser.add_argument("-r", "--report",
                    help="", action="store_true")
parser.add_argument("-fo", "--figures_only",
                    help="export figures only for 'paper' processing", action="store_true")
parser.add_argument("-js", "--journal_submission",
                    help="format for submitting to journals for 'paper' processing", action="store_true")
parser.add_argument('-ws', "--with_supplementary",
                    help="add supplementary for 'paper' processing", action="store_true")

# export format
parser.add_argument("-ef", "--export_format",
                    help="Export format, either: pdf or docx", default='pdf')
parser.add_argument("--with_doc_export",
                    help="Export format, either: pdf or docx", action="store_true")

# manuscript formating options:
parser.add_argument("-fk", "--figure_key",
                    help="Type of references to figures: either 'Figure' of 'Fig.' ", default='Fig.')
parser.add_argument("-ek", "--equation_key",
                    help="Type of references to equations: either 'Equation' of 'Eq.' ", default='Eq.')
parser.add_argument("-tk", "--table_key",
                    help="Type of references to tables: either 'Table' of 'Tab.' ", default='Table')
parser.add_argument("-ak", "--and_key",
                    help="Type of 'and' sign: either '&' or 'and' in plain text", default='and')
parser.add_argument("-abk", "--abstract_key",
                    help="either: 'Summary' or 'Abstract' ...  ", default='Summary')
parser.add_argument("-rk", "--references_key",
                    help="either: 'References' or 'Bibliography' ...  ", default='References')
parser.add_argument("-kpk", "--keypoints_key", default='Key Points')
parser.add_argument("-sk", "--significance_key", default='Significance Statement')
parser.add_argument("-suk", "--supp_key", default='Supplementary Material')


parser.add_argument("--citation_style",
                    help="number / text ", type=str, default='text')
parser.add_argument("--reference_style",
                    help="APA / [...] ", type=str, default='APA')

parser.add_argument("--insert_informations_at_the_end",
                    help="", action="store_true")

parser.add_argument("-p", "--print",
                    help="print the tex file", action="store_true")
parser.add_argument("--debug",
                    help="", action="store_true")
parser.add_argument("--debug_draft",
                    help="", action="store_true")
parser.add_argument("--draft",
                    help="", action="store_true")

args = parser.parse_args()

# args.tex_file = os.path.join('tex', os.path.basename(args.filename).replace('.txt', '.tex'))
# args.pdf_file = os.path.join('tex', os.path.basename(args.filename).replace('.txt', '.pdf'))

# PAPER = paper.process_manuscript(args)
# functions.export_to_pdf(args)


# if args.filename.endswith('.bib'):
#     if 'build' in args.processing:
#         with open(args.filename) as f:
#             txt = f.read()
#         DUPLICATES = biblio.build_library(txt, args)
#     elif 'duplicates' in args.processing:
#         print('[...] clean the biblio.bib file')
#         DUPLICATES = biblio.find_duplicates(verbose=True)
#     else:
#         print('provide an intruction argument to process the bibtex file, either: ')
#         print('   "python your_biblio.bib build" ')
#         print('   "python your_biblio.bib find_duplicates" ')
        
#     print(args.filename)


# if args.filename.endswith('.bib'):
#     if args.build:
#         DUPLICATES = build_library()
#     elif args.find_duplicates:
#         print('[...] clean the biblio.bib file')
#         DUPLICATES = find_duplicates(verbose=True)
# elif args.filename.endswith('.txt') or args.filename.endswith('.org'):
#     process_manuscript(args)
#     export_to_pdf(args)
#     # if args.with_doc_export:
#     #     export_to_docx(args)
#     # else:
# else:
#     print('provide a txt file as an argument')
#     print('   "python your_paper.txt " ')
    
