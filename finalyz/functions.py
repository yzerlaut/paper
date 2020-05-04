import numpy as np
import string, os

#########################################################################
########## PREAMBLE INFORMATIONS ########################################
#########################################################################

def transform_preamble_and_informations_into_title_props(PAPER, args):
    LINES = PAPER['Preamble'].split('\n')


#########################################################################
########## HANDLING MANUSCRIPT INFORMATIONS #############################
#########################################################################

def process_preamble_and_informations(PAPER,
                                      args,
                                      INFORMATION_KEYS):
    """
    we use the preamble of the Informations section to extract the manusrpit information:

    #+Title: This is the study title

    ** Informations
    *** Title
    This is the study title
    """

    # starting with the 'Informations' section
    SUBSECTIONS = PAPER['Informations'].split('\n*')[1:]

    for subsec in SUBSECTIONS:

        for key in INFORMATION_KEYS:
            if len(subsec.split('** %s\n' % key))>1:
                PAPER[key] = subsec.split('** %s\n' % key)[1].replace('\n', '')
                
    # but over-ridden by what lies in the preamble of the file
    LINES = PAPER['Preamble'].split('\n')
    
    for line in LINES:

        for key in INFORMATION_KEYS:
            if len(line.split('#+%s: ' % key))>1:
                PAPER[key] = line.split('#+%s: ' % key)[1]

                
    # HANDLING AUTHORS
    PAPER['Authors'] = PAPER['Authors'].replace('}', '}$').replace('{', '$^{')

    # HANDLING AFFILIATIONS
    aaff = PAPER['Affiliations']
    for i in range(30):
        aaff = aaff.replace('{'+str(i)+'} ', '\\textbf{\\textsuperscript{'+str(i)+'}}')
    PAPER['Affiliations'] = aaff
    # HANDLING Correspondence
    PAPER['Correspondence'] = PAPER['Correspondence'].replace('[[', '\\mailto{').replace(']]', '}')

    for key in INFORMATION_KEYS:
        if key not in PAPER:
            PAPER[key] = '[...]'
    

            
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
    Constructs the LateX table string to insert in the 
    """
    
    if ('extent' in TAB) and TAB['extent']=='double-column':
        TAB['latex_code'] = '\\begin{table*}[tb!]\n'
    else:
        TAB['latex_code'] = '\\begin{table}[tb!]\n'

    if ('hrule_top' in TAB) and TAB['hrule_top']:
        TAB['latex_code'] += '\\hrule \n \\vspace{.1cm} \n'

    TAB['latex_code'] += '\\centering \\small \n'+TAB['table_latex_code']+'\n'
    if args.cross_ref:
        TAB['latex_code'] += ' \\caption{ \\label{tab:'+TAB['label']+'} \n \small \\bfseries '+\
                            TAB['caption_title']+ ' \\normalfont '+TAB['caption_text']+' \\normalsize }\n'
    else:
        TAB['latex_code'] += ' \\caption{ \small \\bfseries '+args.table_key+'\,'+str(TAB['number']+1)+'. '+\
                            TAB['caption_title']+ ' \\normalfont '+TAB['caption_text']+' \\normalsize }\n'
        
    if ('hrule_bottom' in TAB) and TAB['hrule_bottom']:
        TAB['latex_code'] += '\\vspace{.05cm}\n \\hrule \n'
        
    TAB['latex_code'] += '\\normalsize \n'
    if ('extent' in TAB) and TAB['extent']=='double-column':
        TAB['latex_code'] += '\\end{table*}\n'
    else:
        TAB['latex_code'] += '\\end{table}\n'



def process_tables(PAPER, args):
    """
    Analyze the Tables section

    constructs the latex code for the table formatting
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
        PAPER['text'] += '\n  \subsection*{Tables} \n'
        for Table in PAPER['TABLES']:
            PAPER['text'] += '\\qquad \n \centering '
            PAPER['text'] += Table['latex_code']
            PAPER['text'] += '\\newpage \n '
            
    if len(PAPER['FIGS'])>0:
        PAPER['text'] += ' \n \subsection*{Figures} \n'
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


default_fig = {
    'extent':'double-column',
    'width': 1.,
    'scale': 1.,
    'height': 10.,
    'wrapfig': False,
    'hrule_bottom': False,
    'hrule_top': False,
    'page_position': 'tb!',
    'wrapfig_space_before': 0.,
    'wrapfig_space_after':0.,
    'wrapfig_space_left':0.,
    'wrapfig_space_right':0.,
}

oneandahalfcol_fig = {
    'scale': 1.,
    'height': 10.,
    'wrapfig': True,
    'hrule_bottom': False,
    'hrule_top': False,
    'page_position': 'tb!',
    'wrapfig_space_before': 0.,
    'wrapfig_space_after':0.,
    'wrapfig_space_left':0.,
    'wrapfig_space_right':0.,
}

def analyze_fig(FIG):

    if ('extent' in FIG) and (FIG['extent']=='one-and-a-half-column'):
        if 'width' not in FIG:
            FIG['width'] = 0.66
        if 'wrapfig' not in FIG:
            FIG['wrapfig'] = True
            
    for key, default_value in default_fig.items():
        if key not in FIG:
            FIG[key] = default_value
    
def insert_figure(PAPER, FIG, args,
                  supplementary=False):
    """
    Constructs the LateX figure string to insert in the manuscript
    """

    analyze_fig(FIG)
    
    FIG['detailed_caption'] = process_detailed_caption(FIG['detailed_caption'])
    
    if (FIG['extent']=='single-column') or args.figures_only or args.manuscript_submission:
        figure = 'figure'
    else:
        figure = 'figure*'

    figure_text = '\\begin{'+figure+'}[%s]\n' % FIG['page_position']

    if supplementary:
        figure_key = args.figure_key+'\,S'
    else:
        figure_key = args.figure_key+'\,'

    if not args.cross_ref: # most simple version
        figure_text += '\\centering \\begin{singlespace} \n'
        # figure_text += '\\vspace{-1cm}\n' # to stretch a bit the vertical spacing
        figure_text += '\\includegraphics[scale=1.]{'+FIG['file']+'}\n'                       
        figure_text += '\\caption{ \small \\bfseries '+figure_key+str(FIG['number']+1)+'. '+FIG['caption_title']+\
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
        if FIG['hrule_top']:
            figure_text += '\\hrule  \n \\vspace{-.15cm}\n '
        figure_text += '\\captionsetup{labelformat=empty,font=small}'
        figure_text += '\\caption{\\label{fig:'+FIG['label']+'} \\vspace{-2em} }'
        figure_text += '\\begin{wrapfigure}['+str(FIG['height'])+']{l}{'+str(FIG['width'])+'\linewidth}\n'
        figure_text += '\\hspace*{'+str(FIG['wrapfig_space_left'])+'em}\n'
        figure_text += '\\includegraphics[scale='+str(FIG['scale'])+']{'+\
                                                 FIG['file']+'}\n'
        figure_text += '\\end{wrapfigure}\n'
        figure_text += '\\small \\bfseries Figure \\ref*{fig:'+FIG['label']+'}. '+\
                       FIG['caption_title']+\
                       ' \\normalfont '+FIG['detailed_caption']+' \\normalsize \n'
        if FIG['hrule_bottom']:
            figure_text += '\\vspace{.2cm}\n \\hrule \n'
    else:
        figure_text += '\\centering\n'
        if FIG['hrule_top']:
            figure_text += '\\hrule \n '
        figure_text += '\\vspace{'+str(FIG['wrapfig_space_before'])+'em}\n'
        figure_text += '\\includegraphics[scale='+str(FIG['scale'])+']{'+\
                                                 FIG['file']+'}\n'
        figure_text += '\\vspace{'+str(FIG['wrapfig_space_after'])+'em}\n'
        figure_text += '\\caption{ \\label{fig:'+FIG['label']+'} \n \small \\bfseries '+\
                       FIG['caption_title']+\
                       ' \\normalfont '+FIG['detailed_caption']+' \\normalsize }\n'
        if FIG['hrule_bottom']:
            figure_text += '\\vspace{.1cm}\n \\hrule \n'
        
    figure_text += '\\end{'+figure+'}\n'

    FIG['latex_code'] = figure_text

def process_figures(PAPER, args,
                    supplementary=False):
    """
    Analyze the Figures section

    constructs the latex code for the figure formatting
    """
    if supplementary:
        s_Figures = 'Supplementary Figures'
        s_FIGS = 'SUPP_FIGS'
    else:
        s_Figures = 'Figures'
        s_FIGS = 'FIGS'
        
    FIGURES = PAPER[s_Figures].split('\n*** ')[1:] # separator
    for text in FIGURES:
        lines = text.split('\n')
        exec("global params; params = "+lines[1].split('#+options : ')[1])
        params['caption_title'] = lines[0]
        params['detailed_caption'] = ''
        for line in lines[2:]:
            params['detailed_caption'] += line+' '
        params['number'] = len(PAPER[s_FIGS])
        PAPER[s_FIGS].append(params)

    for fig in PAPER[s_FIGS]:
        insert_figure(PAPER, fig, args, supplementary=supplementary)


def replace_text_indication_with_latex_fig(PAPER, args):
    """
    we replace the annotations in the text as:
             [[Figure {Fig1} around here]]
    with the latex code
    """
    for fig in PAPER['FIGS']:
        PAPER['text'] = PAPER['text'].replace('[[Figure {'+fig['label']+'} around here]]', '\n'+fig['latex_code']+'\n')

def include_figure_cross_referencing(PAPER, args,
                                     supplementary=False):
    """
    """

    if supplementary:
        s_FIGS = 'SUPP_FIGS'
        figure_key = args.figure_key+'\,S'
    else:
        s_FIGS = 'FIGS'
        figure_key = args.figure_key+'\,'
        
    for fig in PAPER[s_FIGS]:
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
                                                  fig['label']+'}]{'+figure_key+'\\ref*{fig:'+fig['label']+'}'+to_be_added+'}'+to_be_kept)
            else:
                PAPER['text'] = PAPER['text'].replace(figure_string+next_string, figure_key+str(fig['number']+1)+next_string)
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
    PAPER['Key Points'] = PAPER['Key Points'].replace('Key Points\n', '')
    PAPER['Other'] = ''

    
def process_main_text(PAPER, args):

    txt = '\\vspace{.3cm} \n'
    for line in PAPER['Main Text'].split('\n'):
        if len(line.split('***'))==1:
            txt += '\n'+line
    txt += '\n'

    PAPER['Main Text'] = txt.replace('Main Text\n', '')
    
    
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

def insert_abstract(PAPER, args):

    if args.abstract_key!='':
        PAPER['text'] += '\n\\bfseries \subsection*{%s} \n' % args.abstract_key
    else:
        PAPER['text'] += '\n\\bfseries \n'
    PAPER['text'] += PAPER['Abstract']+'\n'
    PAPER['text'] += '\n \\normalfont \n'
    
def insert_significance(PAPER, args):
    
    PAPER['text'] += '\n\\begin{figure}[b!] \n'
    PAPER['text'] += '\n\\fcolorbox{black}{lightgray}{\\begin{minipage}{.48\\textwidth} \n'
    PAPER['text'] += ' \\textbf{%s} \\ \\vspace{.2em} \n'  % args.significance_key
    PAPER['text'] += PAPER['Significance']
    PAPER['text'] += '\n \\end{minipage} \\normalfont }\n'
    PAPER['text'] += '\n \\end{figure}  \n'

def insert_key_points(PAPER, args):
    
    if args.keypoints_key!='':
        PAPER['text'] += '\n\\bfseries \subsection*{%s} \n' % args.keypoints_key
    else:
        PAPER['text'] += '\n\\bfseries \n'
    PAPER['text'] += '\n\\begin{itemize}\n'
    PAPER['text'] += PAPER['Key Points']
    PAPER['text'] += '\n\\end{itemize}\n'
    PAPER['text'] += '\n \\normalfont \n'

    
def insert_supplementary(PAPER, args):

    PAPER['text'] += '\n \\newpage \n '
    PAPER['text'] += '\\section*{%s} \n ' % args.supp_key
    
    # if PAPER['Supplementary']!='':
    #     PAPER['text'] += '\n \\newpage \n '
    #     PAPER['text'] += PAPER['Supplementary']
    # elif ('Supplementary Figures' in PAPER):
    #     PAPER['text'] += '\n \\newpage \n '
    #     PAPER['text'] += '\\section*{Supplementary Material} \n '
    #     for fig in PAPER['SUPP_FIGS']:
    #         PAPER['text'] += '\n '
    #         PAPER['text'] += fig['latex_code']


def insert_informations_at_the_end(PAPER, args):
    
    PAPER['text'] += '\n \small \\normalfont \\vspace{.1cm}  \n'
    for key in ['Acknowledgements',
                'Funding',
                'Conflict_of_interest',
                'Data_availability']:
        PAPER['text'] += PAPER[key]+'\n \n '
        
        
    
#####################################################################
########## EXPORT OPTIONS ###########################################
#####################################################################

        
def export_to_pdf(args):
    os.system('if [ -d "tex/" ]; then echo ""; else mkdir tex/; fi;')
    if args.debug or args.debug_draft:
        os.system('pdflatex -output-directory=tex/ %s' % args.tex_file)
    else:
        os.system('pdflatex -shell-escape -interaction=nonstopmode -output-directory=tex/ %s > tex/compil_output' % args.tex_file)
    os.system('mv %s %s' % (args.pdf_file, os.path.basename(args.pdf_file)))

def export_to_docx(args):
    """
    needs pandoc
    """
    os.system('if [ -d "tex/" ]; then echo ""; else mkdir tex/; fi;')
    tex_file = args.filename.replace('.txt', '.tex')
    docx_file = args.filename.replace('.txt', '.docx')
    os.system('pandoc '+tex_file+' -o '+docx_file)

    
#####################################################################
########## MANUSCRIPT ANALYSIS ######################################
#####################################################################

def final_manuscript_analysis(PAPER, args):

    PAPER['Num_of_Tables'] = len(PAPER['TABLES'])
    PAPER['Num_of_Figures'] = len(PAPER['FIGS'])

    
if __name__=='__main__':

    analysis = {'stat_test_example': 'c=0.5, p=0.003, Pearson correlation',
                'data_output':'34$\pm$17.3mV'}
    
    np.savez('analysis.npz', **analysis)
