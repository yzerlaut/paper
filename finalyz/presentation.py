"""
We start from a txt file compatible with the org-mode format and want to export it to a tex file
"""
import os, pathlib
import numpy as np

from .tex_templates import BEAMER_CLASS, BEAMER_TEMPLATE
from .functions import *

INFORMATION_KEYS = ['Title', 'Subtitle', 'Short_Title', 'Date',
                    'Authors', 'Short_Authors', 'Affiliations',
                    'with_titlepage']

PRES = {'text':'', # full text
        'Preamble':'',
        'Informations':'',
        'Affiliations':'',
        'Correspondence':''}

# adding informations section
for key in INFORMATION_KEYS:
    PRES[key] = ''


def layer_png(base_dir, figname, index):
    return os.path.join(base_dir,'slides', 'pngs', '%s-layer%i.png' %\
                                            (figname, index))

def include_graphics(png, visible=1):
    """
    """
    latex_code = '\only<%i> { \\node (0,0) { \\hspace{-0.5em} \includegraphics[width=\paperwidth]{%s}} } \n' % (visible, png)
    return latex_code

def add_images_on_slide(subsection, PRES, base_dir):

    location = subsection.split(']]')[0].split('[[')[1]
    filename = location.split(os.path.sep)[-1]


    PRES['text'] += '\\begin{frame}{}\n'
    PRES['text'] += '\\vspace*{-3mm}'
    PRES['text'] += '\\begin{overlayarea}{\\textwidth}{\\textheight}\n'
    PRES['text'] += '\\begin{tikzpicture}\n'
    PRES['text'] += '\hspace*{-1.1cm}'

    if '<!---' in subsection:

        # this means ANIMATIONS

        exec(subsection.split('\n-->')[0].split('<!---\n')[1], globals())

        for a, layers in enumerate(anim):
            for l in layers:
                PRES['text'] += include_graphics(layer_png(base_dir, filename, l), visible=a+1)

    else:
        PRES['text'] += include_graphics(layer_png(base_dir, filename, 1))

    PRES['text'] += '\\end{tikzpicture}\n'
    PRES['text'] += '\\end{overlayarea}\n'
    PRES['text'] += '\\end{frame}{}\n\n'

def process_presentation(args):

    # extracting the full text from the manuscript
    with open(args.filename) as f:
        content = f.readlines()
        full_text = ''
        for c in content:
            full_text+=c

    # organizing the text, secion by section
    SECTIONS = full_text.split('\n# ') # separator for the start of a given section in markdown

    ####### PREAMBLE ##########
    PRES['Preamble'] = SECTIONS[0] # text above the section is the preamble

    process_preamble_and_informations(PRES, args, INFORMATION_KEYS)


    if not ('False' in PRES['with_titlepage']):
        PRES['text'] += '\\section*{{\\quad}}'
        PRES['text'] += '\\begin{{frame}}{{}}'
        PRES['text'] += '    \\maketitle'
        PRES['text'] += '\\end{{frame}}'
        PRES['text'] += '\\end{frame}{}\n\n'

    istart=1

    if ('Table of content' in SECTIONS[istart]) or ('Outline' in SECTIONS[istart]):
        PRES['text'] += '\\begin{frame}{}\n'
        for l in SECTIONS[istart].split('\n')[1:]:
            PRES['text'] += l+'\n'
        PRES['text'] += '\\end{frame}{}\n\n'
        istart+=1

    for isec in range(istart, len(SECTIONS)):
        section = SECTIONS[isec].split('\n')[0]

        if 'thanks' in section:
            PRES['text'] += '\\section*{\\quad}\n'
        else:
            PRES['text'] += '\\section{%s}\n' % section

        for subsection in SECTIONS[isec].split('\n## ')[1:]:

            PRES['text'] += '\\subsection{%s}\n' % subsection.split('\n')[0]

            if '[[' in subsection:
                # this means a slide from inkscape
                add_images_on_slide(subsection, PRES,
                                    os.path.dirname(args.filename))
            else: # we just paste the content into frames
                PRES['text'] += '\\begin{frame}{}\n'
                for l in subsection.split('\n')[1:]:
                    PRES['text'] += l+'\n'
                PRES['text'] += '\\end{frame}{}\n\n'


    if not os.path.isdir('tex'):
        os.mkdir('tex')

    with open('tex/simple.cls', 'w') as f:
        txt = BEAMER_CLASS.format(**PRES)
        f.write(str(txt))

    with open(args.tex_file, 'w') as f:
        txt = BEAMER_TEMPLATE.format(**PRES)
        f.write(str(txt))

    return PRES


def export_svg_layers_to_png(filename, dpi=96):
    """
    """

    slides_dir = os.path.join(os.path.dirname(os.path.abspath(filename)), 'slides')

    pngs_dir = os.path.join(os.path.dirname(os.path.abspath(filename)), 'slides', 'pngs')

    os.system('mkdir %s -p' % pngs_dir)

    SVG_FILES = [f for f in os.listdir(slides_dir) if f.endswith('.svg')]

    bash_script=os.path.join(str(pathlib.Path(__file__).resolve().parent), 'layers2png.sh')

    for svg in SVG_FILES:

        print('\n -- exporting layers for "%s" [...]' % svg)

        bash_code = """
        /bin/bash -c \"source %s; layers2png %s %s %s\" """ % (bash_script,
                                                               os.path.join(slides_dir, svg),
                                                               os.path.join(pngs_dir, svg.replace('.svg','')),
                                                               dpi)
        # print(bash_code)
        os.system(bash_code)


if __name__=='__main__':

    import argparse
    parser=argparse.ArgumentParser(description=
     """
     A script to export presentation txt files to beamer presentations
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
