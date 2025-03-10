import sys
import numpy as np


def remove_complex_characters_in_string(s):
    s2 = s.translate({ord(x): '' for x in ['\v', '^', '~', '{', '}', '\\', '"', "'", '`']})
    return s2


def build_doi_url(entry):
    if 'doi' in entry:
        return "https://doi.org/"+entry['doi']
    else:
        return ''

    
def build_apa_citation(entry):

    citation = ''
    
    authors = ''
    for i, auth in enumerate(entry['author'].split(' and ')):
        lastname = auth.split(',')[0]
        firstnames = auth.split(',')[1].split(' ')
        authors += lastname+' '
        for fn in firstnames:
            if fn:
                authors += fn[0]+'.'
        # we add the comma separation
        authors += ', '
    authors = authors[:-2]+' ' # we remove the last 2 characters
    if i==1: # means only two authors
        authors = authors.replace(', ', ' and ')

    citation += authors
    if 'year' in entry:
        citation += "(%s)" % entry['year']
    else:
        print('"year" field missing in ', entry)

    if 'title' in entry:
        if (entry['title'].endswith('. ')):
            citation += " %s " % entry['title']
        elif (entry['title'].endswith('.')):
            citation += " %s " % entry['title']
        else:
            citation += " %s. " % entry['title']
    else:
        print('"title" field missing in ', entry)

    for key in ['journal', 'volume', 'number', 'pages']:
        if key not in entry:
            entry[key] = ''
        
    if entry['ref_type'] in ['book', 'Book', 'BOOK']:
        if 'publisher' in entry:
            citation += " \\textit{%s}" % entry['publisher']
        else:
            print('"publisher" field missing in ', entry)
            
    elif entry['ref_type'] in ['article', 'Article', 'ARTICLE']:
        if entry['number']:
            citation += '\\textit{{{journal} {volume}}}({number}) {pages} '.format(**entry)
        else:
            citation += '\\textit{{{journal} {volume}}} {pages} '.format(**entry)
            
    return citation


def build_library(Reference_text, args,
                  verbose=False, find_duplicates=False):

    Ref_bases = Reference_text.split('\n@')[1:-1] # the last one is a jabref section

    LIBRARY = {}

    for ref in Ref_bases:

        ref_type = ref.split('{')[0]
        key = ref.split('{')[1].split(',')[0]
        if '_et_al_' in key:
            ref_key = key.replace('_et_al_', ' et al., ')
            intext_key = key.replace('_et_al_', ' et al. (')+')'
        elif '_and_' in key:
            ref_key = key.replace('_and_', ' %s ' % args.and_key).replace('_', ', ')
            intext_key = key.replace('_and_', ' %s ' % args.and_key).replace('_', ' (')+')'
        elif '_' in key:
            ref_key = key.replace('_', ', ')
            intext_key = key.replace('_', ' (')+')'
        else:
            ref_key = ''
            intext_key = ''

        LIBRARY[key] = {'parenthesis_key':ref_key,
                        'intext_key':intext_key,
                        'ref_type':ref_type}

        for line in ref.split('\n')[1:]:
            try:
                field0, value0 = line.split('=')
                field = field0.replace(' ', '')
                value = value0.split('{')[1].replace('},', '')
                LIBRARY[key][field] = value
            except (ValueError, IndexError):
                pass
                # print(field0, value0)

        try:
            LIBRARY[key]['apa'] = build_apa_citation(LIBRARY[key])
            LIBRARY[key]['doi'] = build_doi_url(library[key])
            print(key, ' succeded [ok]')
        except BaseException as be:
            LIBRARY[key]['apa'] = key
            LIBRARY[key]['doi'] = ''
            print(LIBRARY[key]['apa'], ' failed [X]')
            print(build_doi_url(LIBRARY[key]))
            print(ref)
        
    return LIBRARY


#########################################################################
########## HANDLING REFERENCES ##########################################
#########################################################################

            
def process_references(PAPER, args):
    """
    finds the references within the text and replaces them with the accurate ones 
    """

    LIBRARY = build_library(PAPER['References'], args)

    PAPER['References'] = '\n \small \\normalfont \n'
    if args.references_key:
        PAPER['References'] += '\n \subsection*{References} \n'
    else:
        PAPER['References'] += '\n \\vspace{.3cm} \n'
        

    REFS = {'key':[],
            'positions_in_text':[],
            'numbers':[],
            'ParenthesisRef':[],
            'full_ref':[],
            'ParenthesisRef_corrected':[],
            'InTextRef':[],
            'InTextRef_corrected':[]}
    
    # looping over references
    for ref in LIBRARY.keys():
        if (len(PAPER['text'].split(LIBRARY[ref]['parenthesis_key']))>1) or\
           (len(PAPER['text'].split(LIBRARY[ref]['intext_key']))>1):
            REFS['key'].append(ref) # bibtex key of the ref (in * References)
            REFS['ParenthesisRef'].append(LIBRARY[ref]['parenthesis_key'])
            REFS['ParenthesisRef_corrected'].append(LIBRARY[ref]['parenthesis_key']) # here you can modify 
            REFS['InTextRef'].append(LIBRARY[ref]['intext_key'])
            REFS['InTextRef_corrected'].append(LIBRARY[ref]['intext_key'])
            REFS['positions_in_text'].append(len(PAPER['text'].split(ref)[0]))
            REFS['full_ref'].append(LIBRARY[ref]['apa'])
            if args.cross_ref and (LIBRARY[ref]['doi']!=''):
                REFS['full_ref'][-1] += ' \\href{'+LIBRARY[ref]['doi']+'}{[link]}'
            elif args.cross_ref and ('url' in LIBRARY[ref]):
                REFS['full_ref'][-1] += ' \\href{'+LIBRARY[ref]['url']+'}{[link]}'
                
    if args.citation_style=='number':
        REFS['numbers'] = np.argsort(REFS['positions_in_text'])
        REFS['ParenthesisRef_corrected'] = ['[[['+str(ii+1)+']]]' for ii in REFS['numbers']]
    else:
        REFS['numbers'] = np.argsort(REFS['ParenthesisRef'])

    for i0, i in enumerate(REFS['numbers']):
        
        if args.cross_ref:

            if args.citation_style=='number':
                # we test the three parenthesis cases
                for s_before, s_after, s_bef_new, s_aff_new in zip(['(', '(', '; ', '; ', ''],
                                                                   [')', '', ')', '', ''],
                                                                   ['[', '[', ',', ',', ''],
                                                                   [']', '', ']', '', '']):
                    PAPER['text'] = PAPER['text'].replace(s_before+REFS['ParenthesisRef'][i]+s_after,
                                                          s_bef_new+'\\hyperlink{'+REFS['key'][i]+'}{'+str(i0+1)+'}}'+s_aff_new)
                PAPER['text'] = PAPER['text'].replace(REFS['InTextRef'][i],
                                                      REFS['InTextRef_corrected'][i].replace(' (', '\,(')+\
                                       '[\\hyperlink{'+REFS['key'][i]+'}{'+str(i0+1)+'}]')
                
            elif args.citation_style=='number_exponents':
                # we test the three parenthesis cases
                for s_before, s_after, s_bef_new in zip([' (', ' (', '; ', '; ', ''], [')', '', ')', '', ''],
                                                        ['', '', '\\textsuperscript{,}', '\\textsuperscript{,}', '']):
                    PAPER['text'] = PAPER['text'].replace(s_before+REFS['ParenthesisRef'][i]+s_after,
                                               s_bef_new+'\\textsuperscript{\\hyperlink{'+REFS['key'][i]+'}{'+str(i0+1)+'}}')
                PAPER['text'] = PAPER['text'].replace(REFS['InTextRef'][i],
                                                      REFS['InTextRef_corrected'][i].replace(' (', '\,(')+\
                                       '\\textsuperscript{\\hyperlink{'+REFS['key'][i]+'}{'+str(i0+1)+'}}')

            else:
                PAPER['text'] = PAPER['text'].replace(REFS['ParenthesisRef'][i],
                                                  '\\hyperlink{'+REFS['key'][i]+'}{'+REFS['ParenthesisRef_corrected'][i]+'}')
                PAPER['text'] = PAPER['text'].replace(REFS['InTextRef'][i],
                                                  '\\hyperlink{'+REFS['key'][i]+'}{'+REFS['InTextRef_corrected'][i]+'}')
        else:
            PAPER['text'] = PAPER['text'].replace(REFS['ParenthesisRef'][i], REFS['ParenthesisRef_corrected'][i])
            PAPER['References'] += '\\noindent '+REFS['full_ref'][i]+' \\\\[8pt] '

        ### Now putting it at the end in the references section
        if len(args.citation_style.split('number'))>1:
            PAPER['References'] += '\\noindent \hypertarget{'+REFS['key'][i]+'}{['+str(i0+1)+'] '+REFS['full_ref'][i]+'}  \\\\[8pt] \n'
        else:
            PAPER['References'] += '\\noindent \hypertarget{'+REFS['key'][i]+'}{'+REFS['full_ref'][i]+'}  \\\\[8pt] \n'

    PAPER['text'] += PAPER['References']
        

        


    
if __name__=='__main__':

    import argparse
    parser=argparse.ArgumentParser(description=
     """ 
     Interface to the finalyz program. The script process manuscript and bibliography files.
     """
    ,formatter_class=argparse.RawTextHelpFormatter)

    # filename
    parser.add_argument("filename",
        help='filename (either a ".txt" or a ".md" file or the keyword "new" to start a new document)', type=str)
    parser.add_argument("--bib_file", default='./biblio.bib')
    
    args = parser.parse_args()

    with open(args.bib_file) as f:
        text = f.read()
        LIBRARY = build_library(text, args,
                                verbose=True, find_duplicates=False)

