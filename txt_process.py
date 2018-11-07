"""
We start from a txt file compatible with the org-mode format and want to export it to a tex file
"""
import os
import string
import numpy as np

NEW = []
PAPER = {'text':'', 'refs':{},\
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

def process_detailed_caption(caption):
    new_caption = caption
    for s in string.ascii_lowercase:
        new_caption = new_caption.replace('('+s+')', '\\textbf{('+s+')}')
        new_caption = new_caption.replace('*'+s+'*', '\\textbf{'+s+'}')
    for s in string.ascii_uppercase:
        new_caption = new_caption.replace('('+s+')', '\\textbf{('+s+')}')
        new_caption = new_caption.replace('*'+s+'*', '\\textbf{'+s+'}')
    return new_caption

def process_manuscript(args):
    Supplementary_Flag = False # for Figures
    with open(args.filename) as f:
        content = f.readlines()
        iline = 0
        line = content[iline]
        while (line!='* Notes :noexport:\n') and (iline<len(content)):
            line = content[iline]

            new_line = ''
            # if COMMENT
            if (line[0]=='#'):
                pass # this is a comment
            # IF TITLE
            elif (iline==0):
                PAPER['title'] = line
            # IF SHORT_TITLE
            elif line.split('Short Title: ')[0]=='':
                PAPER['short_title'] = line.replace('Short Title: ', '')
            # IF AUTHORS
            elif line.split('Authors: ')[0]=='':
                PAPER['authors'] = line.split('Authors: ')[1].replace('}', '}$').replace('{', '$^{')
            elif line.split('Short Authors: ')[0]=='':
                PAPER['short_authors'] = line.split('Short Authors: ')[1]
            # IF AFFILIATIONS
            elif line.split('Affiliations: ')[0]=='':
                aaff = line.split('Affiliations: ')[1]
                for i in range(30):
                    aaff = aaff.replace('*'+str(i)+'* ', '\\textbf{\\textsuperscript{'+str(i)+'}}')
                PAPER['affiliations'] = aaff
            # If Correspondence
            elif line.split('Correspondence: ')[0]=='':
                corresp = line.split('Correspondence: ')[1]
                corresp = corresp.replace('[[', '\\mailto{')
                corresp = corresp.replace(']]', '}')
                PAPER['correspondence'] = corresp

            # IF SECTIONS
            elif (line=='* Key Points Summary\n') and not args.figures_only:
                PAPER['text'] += '\\normalsize \\bfseries \n'
                PAPER['text'] += '\subsection*{Key Points Summary}\n'
                PAPER['text'] += '\label{sec:key}\n'
            elif (line=='* Significance statement\n') and not args.figures_only:
                PAPER['text'] += '\\normalsize \\bfseries \n'
                PAPER['text'] += '\subsection*{Significance statement}\n'
            elif (line=='* Abstract\n') and not args.figures_only:
                PAPER['text'] += '\\normalsize \\bfseries \n'
                PAPER['text'] += '\subsection*{Abstract}\n'
            elif (line=='* Introduction\n') and not args.figures_only:
                PAPER['text'] += '\\normalsize \\normalfont \n'
                PAPER['text'] += '\subsection*{Introduction}\n'
            elif (line=='* Results\n') and not args.figures_only:
                PAPER['text'] += '\\normalsize \\normalfont \n'
                PAPER['text'] += '\subsection*{Results}\n'
                PAPER['text'] += '\label{sec:results}\n'
            elif (line=='* Discussion\n') and not args.figures_only:
                PAPER['text'] += '\\normalsize \\normalfont \n'
                PAPER['text'] += '\subsection*{Discussion}'
            elif (line=='* Materials and Methods\n') and not args.figures_only:
                PAPER['text'] += '\small \\normalfont \n'
                PAPER['text'] += '\subsection*{Materials and Methods}\n'
                PAPER['text'] += '\label{sec:methods}\n'
            elif (line=='* References\n') and not args.figures_only:
                PAPER['text'] += '\small \\normalfont \n'
                PAPER['text'] += '\subsection*{References}\n\quad'
                # load libarry reference:
                LIBRARY = np.load('biblio.npz')
                # looping over references
                for ref in LIBRARY.keys():
                    if len(PAPER['text'].split(ref))>1:
                        print(LIBRARY[ref])
                        PAPER['text'] += LIBRARY[ref].item()['APA']+' \\newline \n'
                # iline+=2 # we progress in the lines
                # line = content[iline]
                # while (line[0]!='#') and (line[0]!='*'):
                #     key = line.split(']] ')[0].replace('[[','')
                #     new_key = key.replace('., ', '_').replace(', ', '_').replace(' ', '_')
                #     value = line.split(']] ')[1]
                #     PAPER['refs'][new_key] = key
                #     if args.journal_submission:
                #         PAPER['text'] += value+'\n'
                #     else:
                #         PAPER['text'] += '\n\hypertarget{'+new_key+'}{'+value.replace('\n', '}\n')
                #     iline+=2 # we progress in the lines
                #     line = content[iline]
            elif (line=='* Supplementary Material\n') and args.figures_only:
                Supplementary_Flag = True # for Figures
                PAPER['text'] += '\\beginsupplement \n'
            elif (line=='* Supplementary Material\n'):
                Supplementary_Flag = True # for Figures
                PAPER['text'] += '\\newpage \n'
                PAPER['text'] += '\small \\normalfont \n'
                PAPER['text'] += '\subsection*{Supplementary Material}\n'
                PAPER['text'] += '\label{sec:supp}\n'
                PAPER['text'] += '\\beginsupplement \n'

            # IF FIGURE
            elif (line[:11]=='*** FIGURE:'):
                PAPER['FIGS'].append({'extent':'doublecolumn',
                                      'width':1.,
                                      'scale':1.,
                                      'label':'fig'+str(len(PAPER['FIGS'])+1),
                                      'sidecap':(0,0,0),
                                      'wrapfig':False,
                                      'wrapfig_space_before':0.,
                                      'wrapfig_space_after':0.,
                                      'number':len(PAPER['FIGS'])+1,
                                      'supp':Supplementary_Flag})
                PAPER['FIGS'][-1]['caption_title'] = line.replace('*** FIGURE: ', '').replace('\n', '')
                iline+=1 # we progress in the lines
                if len(content[iline].split('#+options'))>1: # meaning it is an option line
                    exec("global params; params = "+content[iline].split('#+options : ')[1])
                    for key in params.keys():
                        PAPER['FIGS'][-1][key] = params[key]
                    # the first remaining key is the Figure ID
                    iline+=1 # we progress in the lines
                PAPER['FIGS'][-1]['detailed_caption'] = process_detailed_caption(content[iline].replace('\n', ''))
                iline+=1 # we progress in the lines
                PAPER['FIGS'][-1]['figure_filename'] = content[iline].replace('[[','').replace(']]\n','') # we progress in the lines

                if (PAPER['FIGS'][-1]['extent']=='singlecolumn') or args.figures_only:
                    figure = 'figure'
                else:
                    figure = 'figure*'
                    
                if not args.journal_submission:
                    if args.figures_only:
                        PAPER['text'] += '\\hfill \\newpage \n'
                    PAPER['text'] += '\\begin{'+figure+'}[tb!]\n'
                    
                    if PAPER['FIGS'][-1]['sidecap']!=(0,0,0): # meaning using minipage
                        PAPER['text'] += '\\centering\n'
                        PAPER['text'] += '\\begin{minipage}{'+str(PAPER['FIGS'][-1]['sidecap'][0])+'\linewidth}\n'
                        PAPER['text'] += '\\includegraphics[scale='+str(PAPER['FIGS'][-1]['scale'])+']{'+\
                                                                   PAPER['FIGS'][-1]['figure_filename']+'}\n'                       
                        PAPER['text'] += '\\end{minipage}\n'
                        PAPER['text'] += '\\hspace{'+str(PAPER['FIGS'][-1]['sidecap'][1])+'\linewidth}\n'
                        PAPER['text'] += '\\begin{minipage}{'+str(PAPER['FIGS'][-1]['sidecap'][2])+'\linewidth}\n'
                        PAPER['text'] += '\\caption{ \\label{fig:'+PAPER['FIGS'][-1]['label']+'} \n \small \\bfseries '+\
                                     PAPER['FIGS'][-1]['caption_title']+\
                                     ' \\normalfont '+PAPER['FIGS'][-1]['detailed_caption']+' \\normalsize }\n'
                        PAPER['text'] += '\\end{minipage}\n'
                        
                    elif PAPER['FIGS'][-1]['wrapfig']:
                        PAPER['text'] += '\\captionsetup{labelformat=empty,font=small}'
                        PAPER['text'] += '\\caption{\\label{fig:'+PAPER['FIGS'][-1]['label']+'} \\vspace{-2em} }'
                        PAPER['text'] += '\\vspace{'+str(PAPER['FIGS'][-1]['wrapfig_space_before'])+'em}\n'
                        PAPER['text'] += '\\begin{wrapfigure}{l}{'+str(PAPER['FIGS'][-1]['width'])+'\linewidth}\n'
                        PAPER['text'] += '\\includegraphics[scale='+str(PAPER['FIGS'][-1]['scale'])+']{'+\
                                         PAPER['FIGS'][-1]['figure_filename']+'}\n'
                        PAPER['text'] += '\\vspace{'+str(PAPER['FIGS'][-1]['wrapfig_space_after'])+'em}\n'
                        PAPER['text'] += '\\end{wrapfigure}\n'
                        PAPER['text'] += '\\small \\bfseries Figure \\ref{fig:'+PAPER['FIGS'][-1]['label']+'}. '+\
                                         PAPER['FIGS'][-1]['caption_title']+\
                                         ' \\normalfont '+PAPER['FIGS'][-1]['detailed_caption']+' \\normalsize \n'
                        
                    else:
                        PAPER['text'] += '\\centering\n'
                        PAPER['text'] += '\\vspace{'+str(PAPER['FIGS'][-1]['wrapfig_space_before'])+'em}\n'
                        PAPER['text'] += '\\includegraphics[scale='+str(PAPER['FIGS'][-1]['scale'])+']{'+\
                                                                   PAPER['FIGS'][-1]['figure_filename']+'}\n'
                        PAPER['text'] += '\\vspace{'+str(PAPER['FIGS'][-1]['wrapfig_space_after'])+'em}\n'
                        PAPER['text'] += '\\caption{ \\label{fig:'+PAPER['FIGS'][-1]['label']+'} \n \small \\bfseries '+\
                                     PAPER['FIGS'][-1]['caption_title']+\
                                     ' \\normalfont '+PAPER['FIGS'][-1]['detailed_caption']+' \\normalsize }\n'

                    PAPER['text'] += '\\end{'+figure+'}\n'

            # IF TABLE
            # elif (line[:10]=='*** TABLE:'):
            #     PAPER['TABLES'].append({'extent':'doublecolumn', 'width':'',
            #                             'label':'fig'+str(len(PAPER['TABLES'])+1),
            #                             'sidecap':(0,0,0),
            #                             'number':len(PAPER['TABLES'])+1,
            #                             'supp':Supplementary_Flag})
            #     PAPER['TABLES'][-1]['caption_title'] = line.replace('*** TABLE: ', '').replace('\n', '')
            #     iline+=1 # we progress in the lines
            #     if len(content[iline].split('#+options'))>1: # meaning it is an option line
            #         exec("global params; params = "+content[iline].split('#+options : ')[1])
            #         for key in params.keys():
            #             PAPER['TABLES'][-1][key] = params[key]
            #         # the first remaining key is the Table ID
            #         iline+=1 # we progress in the lines
            #     PAPER['TABLES'][-1]['table_content'] = content[iline].replace('\n', '')

            #     if (PAPER['TABLES'][-1]['extent']=='singlecolumn') or args.figures_only:
            #         table = 'table'
            #     else:
            #         table = 'table*'
                    
            #     if not args.journal_submission:
            #         if args.figures_only:
            #             PAPER['text'] += '\\hfill \\newpage \n'
            #         PAPER['text'] += '\\begin{'+table+'}[tb!]\n'
            #         PAPER['text'] += '\\centering\n'
            #         if PAPER['TABLES'][-1]['sidecap']!=(0,0,0): # meaning using minipage
            #             PAPER['text'] += '\\begin{minipage}{'+str(PAPER['TABLES'][-1]['sidecap'][0])+'\linewidth}\n'
            #         PAPER['text'] += PAPER['TABLES'][-1]['table_content']
            #         if PAPER['TABLES'][-1]['sidecap']!=(0,0,0): # meaning using minipage
            #             PAPER['text'] += '\\end{minipage}\n'
            #             PAPER['text'] += '\\hspace{'+str(PAPER['TABLES'][-1]['sidecap'][1])+'\linewidth}\n'
            #             PAPER['text'] += '\\begin{minipage}{'+str(PAPER['TABLES'][-1]['sidecap'][2])+'\linewidth}\n'
            #         PAPER['text'] += '\\caption{ \\label{table:'+PAPER['TABLES'][-1]['label']+'} \n \small \\bfseries '+\
            #                          PAPER['TABLES'][-1]['caption_title']+' \\normalsize }\n'
            #         if PAPER['TABLES'][-1]['sidecap']!=(0,0,0): # meaning using minipage
            #             PAPER['text'] += '\\end{minipage}\n'
            #         PAPER['text'] += '\\end{'+table+'}\n'
                    
            # IF SUBSECTIONS
            elif (line[:4]=='*** ') and not args.figures_only:
                PAPER['text'] += '\\subsubsection*{'+line.replace('*** ', '')+'}'
                subtitle = line.replace('*** ', '').split(' ')
                new_subtitle = subtitle[0]
                for i in range(min([3,len(subtitle)])):
                    new_subtitle += '_'+subtitle[i]
                PAPER['text'] += '\label{sec:'+new_subtitle+'}\n'

            elif (line!='* Notes :noexport:\n') and not args.figures_only:
                PAPER['text'] += line
            else:
                pass

            iline+=1

    ## LOOPING ON REFERENCES FOR CROSS REFERENCING
    if not args.journal_submission:
        for new_key, key  in PAPER['refs'].items():
            PAPER['text'] = PAPER['text'].replace(key, '\\hyperlink{'+new_key+'}{'+key+'}')
            # now reformatting for the case: in Author et al. (20XX)
            new_string = key.replace(', ', ' (')+')'
            PAPER['text'] = PAPER['text'].replace(new_string, '\\hyperlink{'+new_key+'}{'+new_string+'}')

    ## LOOPING ON FIGURES FOR CROSS REFERENCING
    if not args.journal_submission:
        for fig in PAPER['FIGS']:
            figure_string = 'Figure {'+fig['label']+'}'
            ii, ref_loc = 0, PAPER['text'].find(figure_string)
            while ref_loc>0:
                ii += ref_loc
                next_string = PAPER['text'][ii+len(figure_string):ii+100+len(figure_string)]
                to_be_added, to_be_kept = '', PAPER['text'][ii+len(figure_string):ii+100+len(figure_string)]
                s, jj = next_string[0], 0
                while ((s in string.ascii_lowercase) or (s in string.ascii_uppercase) or (s==',') or (s=='(') or (s==')') or (s=='-')) and (jj<6):
                    to_be_added += s
                    to_be_kept = to_be_kept[1:]
                    jj+=1
                    s = next_string[jj]
                if (jj>0) and (s==' ') and (to_be_added[-1]==','): # to handle the case Figure 3c, while keeping Figure 3c,d
                    to_be_kept = ','+to_be_kept
                    to_be_added = to_be_added[:-1]
                PAPER['text'] = PAPER['text'].replace(figure_string+next_string, '\\hyperref[{fig:'+\
                                                      fig['label']+'}]{'+args.figure_key+'\,\\ref*{fig:'+fig['label']+'}'+to_be_added+'}'+to_be_kept)
                # and find the next occurence
                ref_loc = PAPER['text'][ii:].find(figure_string)
    else:
        # simple substitution with \ref
        for fig in PAPER['FIGS']:
            PAPER['text'] = PAPER['text'].replace('Figure {'+fig['label']+'}', args.figure_key+'\,'+str(fig['number']))
                    
    ## LOOKING FOR REFERENCED TABLES
    table_string = '\label{table:'
    ii, ref_loc = 0, PAPER['text'].find(table_string)
    while ref_loc>0:
        ii += ref_loc+len(table_string)
        next_string = PAPER['text'][ii:ii+100]
        table_label, jj = '', 0
        while next_string[jj]!='}':
            table_label += next_string[jj]
            jj+=1
        PAPER['TABLES'].append(table_label)
        ref_loc = PAPER['text'][ii:].find(table_string)
        
    ## LOOPING ON TABLES FOR CROSS REFERENCING
    for table in PAPER['TABLES']:
        table_string = 'Table {'+table+'}'
        if not args.journal_submission:
            PAPER['text'] = PAPER['text'].replace(table_string,
                                                  '\\hyperref[{table:'+table+'}]{'+\
                                                  args.table_key+'\,\\ref*{table:'+table+'}}')
        else:
            # simple substitution with \ref
            PAPER['text'] = PAPER['text'].replace('Table {'+table+'}', args.table_key+'\,\\ref{table:'+table+'}')
            
    ## LOOKING FOR REFERENCED EQUATIONS
    equation_string = '\label{eq:'
    ii, ref_loc = 0, PAPER['text'].find(equation_string)
    while ref_loc>0:
        ii += ref_loc+len(equation_string)
        next_string = PAPER['text'][ii:ii+100]
        eq_label, jj = '', 0
        while next_string[jj]!='}':
            eq_label += next_string[jj]
            jj+=1
        PAPER['EQS'].append(eq_label)
        ref_loc = PAPER['text'][ii:].find(equation_string)

    ## LOOPING ON EQUATIONS FOR CROSS REFERENCING
    for eq in PAPER['EQS']:
        equation_string = 'Equation {'+eq+'}'
        if not args.journal_submission:
            PAPER['text'] = PAPER['text'].replace(equation_string,
                                                  '\\hyperref[{eq:'+eq+'}]{'+\
                                                  args.equation_key+'\,\\ref*{eq:'+eq+'}}')
        else:
            # simple substitution with \ref
            PAPER['text'] = PAPER['text'].replace('Equation {'+eq+'}', args.equation_key+'\,\\ref{eq:'+eq+'}')
    
    if args.journal_submission:
        # we add the figures at the end
        PAPER['text'] += '\\newpage \\subsection*{Figures} \n'
        for i, fig in enumerate(PAPER['FIGS']):
            PAPER['text'] += '\\begin{center} \\includegraphics{'+fig['figure_filename']+'} \\end{center} \n'
            PAPER['text'] += '\\qquad \\newline \\qquad \\newline \n'
            PAPER['text'] += '\\textbf{ Figure '+str(i+1)+'. '+fig['caption_title']+\
                             '} '+fig['detailed_caption']+'\n'
            PAPER['text'] += '\\qquad \\newpage\n'

    # to remove the org-mode formatting
    PAPER['text'] = PAPER['text'].replace('[[', '')
    PAPER['text'] = PAPER['text'].replace(']]', '')

    if os.path.isfile(args.analysis_output_file):
        for key, val in dict(np.load(args.analysis_output_file)).items():
            PAPER['text'] = PAPER['text'].replace('{'+key+'}', str(val))
    else:
        print('No analysis file used ...')
        print('"'+args.analysis_output_file+'" not found')
    final_text = BASIC_TEX.format(**PAPER)
    with open(args.filename.replace('.txt', '.tex'), 'w') as f:
        if args.journal_submission or args.figures_only:
            final_text = BASIC_TEX.format(**PAPER)
        else:
            final_text = TEX.format(**PAPER)
            f.write(TEX.format(**PAPER))
        if args.print:
            print(final_text)
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
    parser.add_argument('-af', "--analysis_output_file", help="analysis filename", type=str, default='paper.npz')
    parser.add_argument("-r", "--report", help="", action="store_true")
    parser.add_argument("-fo", "--figures_only", help="", action="store_true")
    parser.add_argument("-fk", "--figure_key", help="Type of references to figures: either 'Figure' of 'Fig.' ", default='Fig.')
    parser.add_argument("-ek", "--equation_key", help="Type of references to equations: either 'Equation' of 'Eq.' ", default='Eq.')
    parser.add_argument("-tk", "--table_key", help="Type of references to tables: either 'Table' of 'Tab.' ", default='Table')
    parser.add_argument("-p", "--print", help="print the tex file", action="store_true")
    parser.add_argument("-js", "--journal_submission", help="format for submitting to journals", action="store_true")
    parser.add_argument("-wdoc", "--with_doc_export", help="with Ms-Word export", action="store_true")
    
    args = parser.parse_args()

    process_manuscript(args)
    
    if args.with_doc_export:
        export_to_docx(args)
    else:
        export_to_pdf(args)
    
