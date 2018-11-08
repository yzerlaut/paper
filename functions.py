import numpy as np

#########################################################################
########## PREAMBLE INFORMATIONS ########################################
#########################################################################

def transform_preamble_into_title_props(PAPER, args):
    LINES = PAPER['Preamble'].split('\n')
    for line in LINES:
        new_line = ''
        # if COMMENT
        if (line=='') or (line[0]=='#'):
            pass # this is a comment
        # IF TITLE
        elif line.split('Title: ')[0]=='':
            PAPER['title'] = line.replace('Title: ', '')
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
        else:
            print('-------------------------------')
            print('the following line in the Premable was not recognized: ')
            print(line)

#########################################################################
########## HANDLING FIGURES #############################################
#########################################################################

def process_detailed_caption(caption):
    """
    puts in bold, the references to the subfigure labels
    """
    new_caption = caption
    for s in string.ascii_lowercase:
        new_caption = new_caption.replace('('+s+')', '\\textbf{('+s+')}')
        new_caption = new_caption.replace('*'+s+'*', '\\textbf{'+s+'}')
    for s in string.ascii_uppercase:
        new_caption = new_caption.replace('('+s+')', '\\textbf{('+s+')}')
        new_caption = new_caption.replace('*'+s+'*', '\\textbf{'+s+'}')
    return new_caption

    
def insert_figure(PAPER, FIG, args):
    """
    Constructs the LateX figure string to insert in the 
    """

    for key, default_value in zip(['extent', 'width', 'scale',\
                                   'wrapfig', 'wrapfig_space_before', 'wrapfig_space_after'],
                                  ['doublecolumn', 1., 1., False, 0., 0.]):
        if key not in FIG:
            FIG[key] = default_value
    
    if (FIG['extent']=='singlecolumn') or args.figures_only:
        figure = 'figure'
    else:
        figure = 'figure*'

    figure_text = ''
    figure_text += '\\begin{'+figure+'}[tb!]\n'
                    
    if 'sidecap' in FIG: # meaning using minipage
        figure_text += '\\centering\n'
        figure_text += '\\begin{minipage}{'+str(FIG['sidecap'][0])+'\linewidth}\n'
        figure_text += '\\includegraphics[scale='+str(FIG['scale'])+']{'+\
                                                   FIG['file']+'}\n'                       
        figure_text += '\\end{minipage}\n'
        figure_text += '\\hspace{'+str(FIG['sidecap'][1])+'\linewidth}\n'
        figure_text += '\\begin{minipage}{'+str(FIG['sidecap'][2])+'\linewidth}\n'
        figure_text += '\\caption{ \\label{fig:'+FIG['label']+'} \n \small \\bfseries '+\
                       FIG['caption_title']+\
                       ' \\normalfont '+FIG['detailed_caption']+' \\normalsize }\n'
        figure_text += '\\end{minipage}\n'
                        
    elif ('wrapfig' in FIG) and (FIG['wrapfig']):
        figure_text += '\\captionsetup{labelformat=empty,font=small}'
        figure_text += '\\caption{\\label{fig:'+FIG['label']+'} \\vspace{-2em} }'
        figure_text += '\\vspace{'+str(FIG['wrapfig_space_before'])+'em}\n'
        figure_text += '\\begin{wrapfigure}{l}{'+str(FIG['width'])+'\linewidth}\n'
        figure_text += '\\includegraphics[scale='+str(FIG['scale'])+']{'+\
                                                 FIG['file']+'}\n'
        figure_text += '\\vspace{'+str(FIG['wrapfig_space_after'])+'em}\n'
        figure_text += '\\end{wrapfigure}\n'
        figure_text += '\\small \\bfseries Figure \\ref{fig:'+FIG['label']+'}. '+\
                       FIG['caption_title']+\
                       ' \\normalfont '+FIG['detailed_caption']+' \\normalsize \n'
                        
    else:
        figure_text += '\\centering\n'
        figure_text += '\\vspace{'+str(FIG['wrapfig_space_before'])+'em}\n'
        figure_text += '\\includegraphics[scale='+str(FIG['scale'])+']{'+\
                                                 FIG['file']+'}\n'
        figure_text += '\\vspace{'+str(FIG['wrapfig_space_after'])+'em}\n'
        figure_text += '\\caption{ \\label{fig:'+FIG['label']+'} \n \small \\bfseries '+\
                       FIG['caption_title']+\
                       ' \\normalfont '+FIG['detailed_caption']+' \\normalsize }\n'
        
    figure_text += '\\end{'+figure+'}\n'

    FIG['latex_code'] = figure_text

def process_figures(PAPER, args):
    """
    Analyze the Figures section

    constructs the latex code for the figure formatting
    """
    FIGURES = PAPER['Figures'].split('\n*** ')[1:] # separator
    for text in FIGURES:
        lines = text.split('\n')
        exec("global params; params = "+lines[1].split('#+options : ')[1])
        params['caption_title'] = lines[0]
        params['detailed_caption'] = ''
        for line in lines[2:]:
            params['detailed_caption'] += line+' '
        params['number'] = len(PAPER['FIGS'])
        PAPER['FIGS'].append(params)

    for fig in PAPER['FIGS']:
        insert_figure(PAPER, fig, args)


def replace_text_indication_with_latex_fig(PAPER, args):
    """
    we replace the annotations in the text as:
             [[Figure {Fig1} around here]]
    with the latex code
    """
    for fig in PAPER['FIGS']:
        PAPER['text'] = PAPER['text'].replace('[[Figure {'+fig['label']+'} around here]]', '\n'+fig['latex_code']+'\n')


#########################################################################
########## HANDLING TABLES ##############################################
#########################################################################

def process_tables(PAPER, args):

    FIGURES = PAPER['Tables'].split('\n*** ')[1:] # separator
    for text in FIGURES:
        lines = text.split('\n')
        exec("global params; params = "+lines[1].split('#+options : ')[1])
        params['main_caption'] = lines[0]
        params['detailed_caption'] = ''
        for line in lines[2:]:
            params['detailed_caption'] += line+' '
        PAPER['TABLES'].append(params)
    print(PAPER['TABLES'])
    
    
def process_section_titles(PAPER, args):
    """
    
    """
    PAPER['Methods'] = PAPER['Methods'].replace('Methods\n', '\small \\normalfont \n \subsection*{Materials and Methods}\n \label{sec:methods} \n')
    PAPER['Results'] = PAPER['Results'].replace('Results\n', '\\normalsize \\normalfont \n \subsection*{Results}\n')
    PAPER['Introduction'] = PAPER['Introduction'].replace('Introduction\n', '\\normalsize \\normalfont \n \subsection*{Introduction}\n')
    PAPER['Discussion'] = PAPER['Discussion'].replace('Discussion\n', '\\normalsize \\normalfont \n \subsection*{Discussion}\n')

def process_subsection_titles(PAPER, args):
    """
    
    """
    SUBSECTIONS_HEADS = PAPER['text'].split('\n*** ')
    SUBSECTIONS_TITLES = []
    for sh in SUBSECTIONS_HEADS[1:]:
        SUBSECTIONS_TITLES.append(sh.split('\n')[0])

    for st in SUBSECTIONS_TITLES:
        PAPER['text'] = PAPER['text'].replace('*** '+st, '\subsubsection*{'+st+'} \n')
    

#########################################################################
########## MANUSCRIPT ORGANIZATION ######################################
#########################################################################

def assemble_text(PAPER, args):

    PAPER['text'] = ''

    for key in ['Introduction', 'Results', 'Methods','Discussion']:
        PAPER['text'] += PAPER[key]

    process_subsection_titles(PAPER, args)


#########################################################################
########## HANDLING REFERENCES ##########################################
#########################################################################

            
def process_references(PAPER, args):
    """
    finds the references within the text and replaces them with the accurate ones 
    """
    try:
        LIBRARY = np.load('biblio.npz')
    except FileNotFoundError:
        print('biblio.npz', ' NOT FOUND !')
        LIBRARY = []

    PAPER['References'] = '\n \small \\normalfont \n \subsection*{References} \n'

    REFS = {'key':[], 'positions_in_text':[], 'numbers':[], 'abbrev_in_text':[], 'full_ref':[], 'correct_abbrev':[]}
    # looping over references
    for ref in LIBRARY.keys():
        if len(PAPER['text'].split(ref))>1:
            
            REFS['key'].append(ref.replace('., ', '_').replace(', ', '_').replace(' ', '_'))
            REFS['abbrev_in_text'].append(ref)
            REFS['correct_abbrev'].append(LIBRARY[ref].item()['correct_abbrev'])
            REFS['positions_in_text'].append(len(PAPER['text'].split(ref)[0]))
            REFS['full_ref'].append(LIBRARY[ref].item()['APA'])

    """
    Here you should sort in positions_in_text to number the references in Nature & Plos reference style

    """
    if args.citation_style=='number':
        REFS['numbers'] = np.argsort(REFS['positions_in_text'])
        REFS['correct_abbrev'] = ['[[['+str(ii+1)+']]]' for ii in REFS['numbers']]
    else:
        REFS['numbers'] = np.argsort(REFS['abbrev_in_text'])

    for i0, i in enumerate(REFS['numbers']):
        PAPER['text'] = PAPER['text'].replace(REFS['abbrev_in_text'][i],
                                              '\\hyperlink{'+REFS['key'][i]+'}{'+REFS['correct_abbrev'][i]+'}')
        if args.citation_style=='number':
            PAPER['References'] += '\hypertarget{'+REFS['key'][i]+'}{['+str(i0+1)+'] '+REFS['full_ref'][i]+'} \\newline \n'
        else:
            PAPER['References'] += '\hypertarget{'+REFS['key'][i]+'}{'+REFS['full_ref'][i]+'} \\newline \n'

    if args.journal=='Nature':
        PAPER['text'] = PAPER['text'].replace(' (\\hyperlink{', '$^{\\hyperlink{')
        PAPER['text'] = PAPER['text'].replace(']]]})', '}$')
        PAPER['text'] = PAPER['text'].replace(']]]}; ', '},')
        PAPER['text'] = PAPER['text'].replace('[[[', '')
    elif args.journal=='PloS':
        PAPER['text'] = PAPER['text'].replace(' (\\hyperlink{', '[\\hyperlink{')
        PAPER['text'] = PAPER['text'].replace(']]]})', '}]')
        PAPER['text'] = PAPER['text'].replace(']]]}; ', '},')
        PAPER['text'] = PAPER['text'].replace('[[[', '')

        
    PAPER['text'] += PAPER['References']
        

    
