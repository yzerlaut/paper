import numpy as np

def transform_preamble_into_title_props(PAPER, args):
    LINES = PAPER['Preamble'].split('\n')
    for line in LINES:
        new_line = ''
        # if COMMENT
        if (line[0]=='#') or (line==''):
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

def process_figures(PAPER, args):

    FIGURES = PAPER['Figures'].split('\n*** ')[1:] # separator
    for text in FIGURES:
        lines = text.split('\n')
        exec("global params; params = "+lines[1].split('#+options : ')[1])
        params['main_caption'] = lines[0]
        params['detailed_caption'] = ''
        for line in lines[2:]:
            params['detailed_caption'] += line+' '
        PAPER['FIGS'].append(params)
    print(PAPER['FIGS'])

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
    

    figure_text = ''
    figure_text += '\\begin{'+figure+'}[tb!]\n'
                    
    if 'sidecap' in FIG: # meaning using minipage
        figure_text += '\\centering\n'
        figure_text += '\\begin{minipage}{'+str(FIG['sidecap'][0])+'\linewidth}\n'
        figure_text += '\\includegraphics[scale='+str(FIG['scale'])+']{'+\
                                                   FIG['figure_filename']+'}\n'                       
        figure_text += '\\end{minipage}\n'
        figure_text += '\\hspace{'+str(FIG['sidecap'][1])+'\linewidth}\n'
        figure_text += '\\begin{minipage}{'+str(FIG['sidecap'][2])+'\linewidth}\n'
        figure_text += '\\caption{ \\label{fig:'+FIG['label']+'} \n \small \\bfseries '+\
                       FIG['caption_title']+\
                       ' \\normalfont '+FIG['detailed_caption']+' \\normalsize }\n'
        figure_text += '\\end{minipage}\n'
                        
    elif FIG['wrapfig']:
        figure_text += '\\captionsetup{labelformat=empty,font=small}'
        figure_text += '\\caption{\\label{fig:'+FIG['label']+'} \\vspace{-2em} }'
        figure_text += '\\vspace{'+str(FIG['wrapfig_space_before'])+'em}\n'
        figure_text += '\\begin{wrapfigure}{l}{'+str(FIG['width'])+'\linewidth}\n'
        figure_text += '\\includegraphics[scale='+str(FIG['scale'])+']{'+\
                                                 FIG['figure_filename']+'}\n'
        figure_text += '\\vspace{'+str(FIG['wrapfig_space_after'])+'em}\n'
        figure_text += '\\end{wrapfigure}\n'
        figure_text += '\\small \\bfseries Figure \\ref{fig:'+FIG['label']+'}. '+\
                       FIG['caption_title']+\
                       ' \\normalfont '+FIG['detailed_caption']+' \\normalsize \n'
                        
    else:
        figure_text += '\\centering\n'
        figure_text += '\\vspace{'+str(FIG['wrapfig_space_before'])+'em}\n'
        figure_text += '\\includegraphics[scale='+str(FIG['scale'])+']{'+\
                                                 FIG['figure_filename']+'}\n'
        figure_text += '\\vspace{'+str(FIG['wrapfig_space_after'])+'em}\n'
        figure_text += '\\caption{ \\label{fig:'+FIG['label']+'} \n \small \\bfseries '+\
                       FIG['caption_title']+\
                       ' \\normalfont '+FIG['detailed_caption']+' \\normalsize }\n'
    figure_text += '\\end{'+figure+'}\n'

    
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

    for key in ['Methods', 'References', 'Supp']:
        pass
        
    for key in ['Results', 'Intro','Discussion', 'Points']:
        pass

    try:
        LIBRARY = np.load('biblio.npz')
    except FileNotFoundError:
        print('biblio.npz', ' NOT FOUND !')
        LIBRARY = []
        
    # looping over references
    for ref in LIBRARY.keys():
        
        if len(PAPER['text'].split(ref))>1:
            print(len(PAPER['text'].split(ref)[0]))
            new_key = ref.replace('., ', '_').replace(', ', '_').replace(' ', '_')
            PAPER['text'] = PAPER['text'].replace(ref, '\\hyperlink{'+new_key+'}{'+LIBRARY[ref].item()['correct_abbrev']+'}')
            PAPER['References'] += '\hypertarget{'+new_key+'}{'+LIBRARY[ref].item()['APA']+'} \\newline \n'
    


            
def process_references(PAPER, args):
    """
    finds the references within the text and replaces them with the accurate 
    """
    try:
        LIBRARY = np.load('biblio.npz')
    except FileNotFoundError:
        print('biblio.npz', ' NOT FOUND !')
        LIBRARY = []
        
    # looping over references
    for ref in LIBRARY.keys():
        
        if len(PAPER['text'].split(ref))>1:
            print(len(PAPER['text'].split(ref)[0]))
            new_key = ref.replace('., ', '_').replace(', ', '_').replace(' ', '_')
            PAPER['text'] = PAPER['text'].replace(ref, '\\hyperlink{'+new_key+'}{'+LIBRARY[ref].item()['correct_abbrev']+'}')
            PAPER['References'] += '\hypertarget{'+new_key+'}{'+LIBRARY[ref].item()['APA']+'} \\newline \n'
    
