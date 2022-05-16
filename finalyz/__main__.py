import argparse, os, shutil, pathlib

from . import paper, presentation, letter, functions, biblio, svg

parser=argparse.ArgumentParser(description=
 """ 

 Interface to the finalyz program. The script process manuscript and bibliography files.

 """
,formatter_class=argparse.RawTextHelpFormatter)


# filename
parser.add_argument("filename", help='filename (either a ".txt" or a ".org" file or the keyword "new" to start a new document)', type=str)

# processing type
parser.add_argument('-p', "--processing",
                    help="either:\n      'paper', 'report', 'presentation' \n ", type=str)

# create new document
parser.add_argument("--create_new",
                    help="initialize a new scientific document type", action="store_true")

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
parser.add_argument("-kpk", "--keypoints_key", help='', default='Key Points')
parser.add_argument("-sk", "--significance_key", help='', default='Significance Statement')
parser.add_argument("-suk", "--supp_key", help='', default='Supplementary Material')

parser.add_argument("--citation_style",
                    help="number / text ", type=str, default='text')
parser.add_argument("--reference_style",
                    help="APA / [...] ", type=str, default='APA')

parser.add_argument("--insert_informations_at_the_end",
                    help="", action="store_true")

parser.add_argument("--print",
                    help="print the tex file", action="store_true")
parser.add_argument("--debug",
                    help="", action="store_true")
parser.add_argument("--debug_draft",
                    help="", action="store_true")
parser.add_argument("--draft",
                    help="", action="store_true")

args = parser.parse_args()
args.tex_file = os.path.join('tex', os.path.basename(args.filename).replace('.txt', '.tex'))

if args.create_new:
    
    if ('presentation' in args.filename) or (args.processing=='presentation'):
        shutil.copy(os.path.join(pathlib.Path(__file__).resolve().parents[1], 'templates', 'presentation.txt'), 'presentation.txt')
        if not os.path.isdir('slides'):
            shutil.copytree(os.path.join(pathlib.Path(__file__).resolve().parents[1], 'templates', 'slides'), 'slides', symlinks=False, ignore=None)
    if ('paper' in args.filename) or (args.processing=='paper'):
        shutil.copy(os.path.join(pathlib.Path(__file__).resolve().parents[1], 'templates', 'paper.txt'), 'paper.txt')
    if ('report' in args.filename) or (args.processing=='report'):
        shutil.copy(os.path.join(pathlib.Path(__file__).resolve().parents[1], 'templates', 'report.txt'), 'report.txt')

elif args.filename.endswith('.txt') or args.filename.endswith('.org'):
    
    if (args.processing=='presentation') or (args.filename=='presentation.txt'):
        PRES= presentation.process_presentation(args)
        functions.export_to_pdf(args)
    elif (args.processing=='paper') or (args.filename=='paper.txt'):
        PAPER = paper.process_manuscript(args)
        functions.export_to_pdf(args)
    elif (args.processing=='report') or (args.filename=='report.txt'):
        PAPER = report.process_manuscript(args)
        functions.export_to_pdf(args)
    else:
        print(' "%s" processing is not a valid option' % args.processing)
        print('   -> please pass a valid processing option ("report", "presentation", ...)' % args.processing)
    
else:
    print(' "%s" filename not a valid filename, provide a ".txt" or a ".org" file ' % args.filename)








