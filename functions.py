import numpy as np
import string, os

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
        # If Conflict of Interset
        elif line.split('Conflict of interest: ')[0]=='':
            conflict = line.split('Conflict of interest: ')[1]
            PAPER['conflict_of_interest'] = conflict
        # If Acknowledgments
        elif line.split('Acknowledgements: ')[0]=='':
            conflict = line.split('Acknowledgements: ')[1]
            PAPER['Acknowledgements'] = conflict
        # If Keywords
        elif line.split('Keywords: ')[0]=='':
            PAPER['Keywords'] = line.split('Keywords: ')[1]
        # If Funding
        elif line.split('Funding: ')[0]=='':
            PAPER['Funding'] = line.split('Funding: ')[1]
        else:
            print('-------------------------------')
            print('the following line in the Premable was not recognized: ')
            print(line)

    if 'conflict_of_interest' not in PAPER:
        PAPER['conflict_of_interest'] = 'The authors declare no conflict of interest.'
        
    for key in ['Funding', 'Correspondence']:
        if key not in PAPER:
            PAPER[key] = ' [...] '
    
            
#########################################################################
########## HANDLING EQUATIONS ###########################################
#########################################################################

def process_equations(PAPER, args):

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

    for ne, eq in enumerate(PAPER['EQS']):
        equation_string = 'Equation {'+eq+'}'
        if not args.manuscript_submission:
            PAPER['text'] = PAPER['text'].replace(equation_string,
                                                  '\\hyperref[{eq:'+eq+'}]{'+\
                                                  args.equation_key+'\,\\ref*{eq:'+eq+'}}')
        elif args.cross_ref:
            # simple substitution with \ref
            PAPER['text'] = PAPER['text'].replace('Equation {'+eq+'}', args.equation_key+'\,\\ref{eq:'+eq+'}')
        else:
            PAPER['text'] = PAPER['text'].replace('Equation {'+eq+'}', args.equation_key+'\,'+str(ne+1)) # just text


#########################################################################
########## HANDLING TABLES ##############################################
#########################################################################

def insert_table(PAPER, TAB, args):
    """
    Constructs the LateX figure string to insert in the 
    """
    
    if ('extent' in TAB) and TAB['extent']=='doublecolumn':
        TAB['latex_code'] = '\\begin{table*}[tb!]\n'
    else:
        TAB['latex_code'] = '\\begin{table}[tb!]\n'
        
    TAB['latex_code'] += '\\centering \\small \n'+TAB['table_latex_code']+'\n'
    if args.cross_ref:
        TAB['latex_code'] += ' \\caption{ \\label{tab:'+TAB['label']+'} \n \small \\bfseries '+\
                            TAB['caption_title']+ ' \\normalfont '+TAB['caption_text']+' \\normalsize }\n'
    else:
        TAB['latex_code'] += ' \\caption{ \small \\bfseries '+args.table_key+'\,'+str(TAB['number']+1)+'. '+\
                            TAB['caption_title']+ ' \\normalfont '+TAB['caption_text']+' \\normalsize }\n'
        
    TAB['latex_code'] += '\\normalsize \n'
    if ('extent' in TAB) and TAB['extent']=='doublecolumn':
        TAB['latex_code'] += '\\end{table*}\n'
    else:
        TAB['latex_code'] += '\\end{table}\n'



def process_tables(PAPER, args):
    """
    Analyze the Figures section

    constructs the latex code for the figure formatting
    """
    TABLES = PAPER['Tables'].split('\n*** ')[1:] # separator
    for text in TABLES:
        lines = text.split('\n')
        exec("global params; params = "+lines[1].split('#+options : ')[1])
        params['caption_title'] = lines[0]
        params['caption_text'] = lines[2]
        params['table_latex_code'] = ''
        for line in lines[3:]:
            if (len(line)>1) and (line[0]!='|') and (line[0]!='#'):
                params['table_latex_code'] += line +'\n'
        params['number'] = len(PAPER['TABLES'])
        PAPER['TABLES'].append(params)
        print(params['table_latex_code'])
    for tab in PAPER['TABLES']:
        insert_table(PAPER, tab, args)

def replace_text_indication_with_latex_table(PAPER, args):
    """
    we replace the annotations in the text as:
             [[Table {tab1} around here]]
    with the latex code
    """
    for tab in PAPER['TABLES']:
        PAPER['text'] = PAPER['text'].replace('[[Table {'+tab['label']+'} around here]]', '\n'+tab['latex_code']+'\n')
        

def add_figures_and_tables_at_the_end(PAPER, args):

    if len(PAPER['TABLES'])>0:
        PAPER['text'] += '\\newpage \n  \subsection*{Tables} \n'
        for Table in PAPER['TABLES']:
            PAPER['text'] += '\\qquad \n \centering '
            PAPER['text'] += Table['latex_code']
            PAPER['text'] += '\\newpage \n '
            
    if len(PAPER['FIGS'])>0:
        PAPER['text'] += '\\newpage \n \subsection*{Figures} \n'
        for FIG in PAPER['FIGS']:
            PAPER['text'] += '\\qquad \n \centering '
            PAPER['text'] += FIG['latex_code']
            PAPER['text'] += '\\newpage \n '

            
def include_table_cross_referencing(PAPER, args):
    """
    """
    for tab in PAPER['TABLES']:
        if args.cross_ref:
            PAPER['text'] = PAPER['text'].replace('Table {'+tab['label']+'}', '\\hyperref[{tab:'+\
                                                  tab['label']+'}]{Table\,\\ref*{tab:'+tab['label']+'}}')
        else:
            PAPER['text'] = PAPER['text'].replace('Table {'+tab['label']+'}', args.table_key+'\,'+str(tab['number']+1))
        
        
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

    FIG['detailed_caption'] = process_detailed_caption(FIG['detailed_caption'])
    
    if (FIG['extent']=='singlecolumn') or args.figures_only or args.manuscript_submission:
        figure = 'figure'
    else:
        figure = 'figure*'

    figure_text = '\\begin{'+figure+'}[tb!]\n \\centering \n'
    
    if not args.cross_ref: # most simple version
        figure_text += '\\centering \\begin{singlespace} \n'
        # figure_text += '\\vspace{-1cm}\n' # to stretch a bit the vertical spacing
        figure_text += '\\includegraphics[scale=1.]{'+FIG['file']+'}\n'                       
        figure_text += '\\caption{ \small \\bfseries '+args.figure_key+'\,'+str(FIG['number']+1)+'. '+FIG['caption_title']+\
                       ' \\normalfont '+FIG['detailed_caption']+' \\normalsize } \\end{singlespace} \n'
        # figure_text += '\\vspace{-0.5cm}\n' # to stretch a bit the vertical spacing
        
    elif args.manuscript_submission: # with cross referencing
        figure_text += '\\centering \\begin{singlespace} \n'
        figure_text += '\\vspace{-1cm}\n' # to stretch a bit the vertical spacing
        figure_text += '\\includegraphics[scale=1.]{'+FIG['file']+'}\n'                       
        figure_text += '\\caption{ \\label{fig:'+FIG['label']+'} \n \small \\bfseries '+\
                       FIG['caption_title']+\
                       ' \\normalfont '+FIG['detailed_caption']+' \\normalsize }\n'
        figure_text += '\\end{singlespace} \n'
        # figure_text += '\\vspace{1cm}\n' # to stretch a bit the vertical spacing
                    
    elif 'sidecap' in FIG: # meaning using minipage
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

def include_figure_cross_referencing(PAPER, args):
    """
    """

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
                
            if args.cross_ref:
                PAPER['text'] = PAPER['text'].replace(figure_string+next_string, '\\hyperref[{fig:'+\
                                                  fig['label']+'}]{'+args.figure_key+'\,\\ref*{fig:'+fig['label']+'}'+to_be_added+'}'+to_be_kept)
            else:
                PAPER['text'] = PAPER['text'].replace(figure_string+next_string, args.figure_key+'\,'+str(fig['number']+1)+next_string)
            # and find the next occurence
            ref_loc = PAPER['text'][ii:].find(figure_string)
    

#########################################################################
########## HANDLING SECTOINS ##############################################
#########################################################################

def count_words_per_sections(PAPER):
    """
    just using the "space" has the default word separator
    """
    for section in ['Abstract', 'Introduction', 'Discussion', 'Methods', 'Results']:
        PAPER['Num_Words_of_'+section] = str(len(PAPER[section].replace(section+'\n', '').split(' ')))
    
    
    
def process_section_titles(PAPER, args):
    """
    
    """
    # before making latex substitutions, we count the words
    count_words_per_sections(PAPER)
    
    PAPER['Abstract'] = PAPER['Abstract'].replace('Abstract\n', '')
    PAPER['Significance'] = PAPER['Significance'].replace('Significance\n', '')
    PAPER['Methods'] = PAPER['Methods'].replace('Methods\n','\small \\normalfont \n \subsection*{Materials and Methods}\n \label{sec:methods} \n')
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
########## HANDLING REFERENCES ##########################################
#########################################################################

            
def process_references(PAPER, args):
    """
    finds the references within the text and replaces them with the accurate ones 
    """
    try:
        print('USING :', os.environ["DIR"]+os.path.sep+'biblio.npz')
        LIBRARY = np.load(os.environ["DIR"]+os.path.sep+'biblio.npz')
    except FileNotFoundError:
        print(os.environ["DIR"]+'biblio.npz', ' NOT FOUND !')
        LIBRARY = {}

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

    if args.citation_style=='number':
        REFS['numbers'] = np.argsort(REFS['positions_in_text'])
        REFS['correct_abbrev'] = ['[[['+str(ii+1)+']]]' for ii in REFS['numbers']]
    else:
        REFS['numbers'] = np.argsort(REFS['abbrev_in_text'])

    for i0, i in enumerate(REFS['numbers']):
        if args.cross_ref:
            PAPER['text'] = PAPER['text'].replace(REFS['abbrev_in_text'][i],
                                              '\\hyperlink{'+REFS['key'][i]+'}{'+REFS['correct_abbrev'][i]+'}')
        if not args.cross_ref:
            PAPER['text'] = PAPER['text'].replace(REFS['abbrev_in_text'][i], REFS['correct_abbrev'][i])
            # PAPER['References'] += '$\\cdot$ '+REFS['full_ref'][i]+' \\newline \n '
            PAPER['References'] += ' \\qquad '+REFS['full_ref'][i]+' \\newline \n \n \, \\qquad \, \\newline \, '
            
        elif args.citation_style=='number':
            PAPER['References'] += '\hypertarget{'+REFS['key'][i]+'}{['+str(i0+1)+'] '+REFS['full_ref'][i]+'} \\newline \n'
        else:
            PAPER['References'] += '$\\cdot$ \hypertarget{'+REFS['key'][i]+'}{'+REFS['full_ref'][i]+'} \\newline  \n'

    """
    Here we handle the Nature & Plos reference style
    """
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
        

#########################################################################
########## MANUSCRIPT ORGANIZATION ######################################
#########################################################################

def insert_abstract(PAPER, args):

    PAPER['text'] += '\n\\bfseries \subsection*{Abstract} \n'
    PAPER['text'] += PAPER['Abstract']+'\n'
    PAPER['text'] += '\n \\normalfont \n'

    if args.manuscript_submission: # then simple version
        PAPER['text'] += '\n\\bfseries \subsection*{Author Summary} \n'
        PAPER['text'] += PAPER['Significance']+'\n'
        PAPER['text'] += '\n \\normalfont \n'
    else:
        PAPER['text'] += '\n\\begin{figure}[b!]{\\linewidth} \n'
        PAPER['text'] += '\n\\fcolorbox{black}{lightgray}{\\begin{minipage}{\\linewidth} \n'
        PAPER['text'] += ' \\textbf{Author Summary} \\ \\vspace{.2em} \n'
        PAPER['text'] += PAPER['Significance']
        PAPER['text'] += '\n \\end{minipage} \\normalfont }\n'
        PAPER['text'] += '\n \\end{figure}  \n'


def assemble_text(PAPER, args):

    PAPER['text'] = ''

    if not args.figures_only:

        insert_abstract(PAPER, args)
        
        for key in PAPER['order']:
            PAPER['text'] += PAPER[key]
        process_subsection_titles(PAPER, args)
        
    else:
        for FIG in PAPER['FIGS']:
            PAPER['text'] += '\\qquad \n '
            PAPER['text'] += FIG['latex_code']
            PAPER['text'] += '\\newpage \n '
        

def final_manuscript_analysis(PAPER, args):

    PAPER['Num_of_Tables'] = len(PAPER['TABLES'])
    PAPER['Num_of_Figures'] = len(PAPER['FIGS'])

    
if __name__=='__main__':

    analysis = {'stat_test_example': 'c=0.5, p=0.003, Pearson correlation', 'data_output':'34$\pm$17.3mV'}
    np.savez('analysis.npz', **analysis)
