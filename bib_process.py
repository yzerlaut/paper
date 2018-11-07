import sys
import bibtexparser as bp
import numpy as np

with open('biblio.bib') as bibtex_file:
    bib_database = bp.load(bibtex_file)

def transform_author_to_list_of_dict(author_field):
    """
    """
    AL = author_field.split(' and ')
    AD = [{'firstname':[], 'lastname':''} for a in AL] # list of dictionary per author
    for d, a in zip(AD, AL):
        names = a.split(',')
        d['lastname'] = names[0].replace(' ', '')
        if len(names)>1:
            for s in names[1].split(' '):
                if (s!=''):
                    d['firstname'].append(s)
    return AD

def get_abbrev_of_entry(list_of_author_dict, entry, find_duplicates=False):
    """
    """
    if ('year2' in entry) and not find_duplicates:
        year = entry['year2'].replace(' ', '')
    else:
        year = entry['year'].replace(' ', '')
    if len(list_of_author_dict)==1:
        return list_of_author_dict[0]['lastname']+', '+year
    elif len(list_of_author_dict)==2:
        return list_of_author_dict[0]['lastname']+' and '+list_of_author_dict[1]['lastname']+', '+year
    else:
        return list_of_author_dict[0]['lastname']+' et al., '+year

def get_intext_abbrev_of_entry(list_of_author_dict, entry):
    """
    """
    if ('year2' in entry) and not find_duplicates:
        year = entry['year2'].replace(' ', '')
    else:
        year = entry['year'].replace(' ', '')
    if len(list_of_author_dict)==1:
        return list_of_author_dict[0]['lastname']+' ('+year+')'
    elif len(list_of_author_dict)==2:
        return list_of_author_dict[0]['lastname']+' and '+list_of_author_dict[1]['lastname']+' ('+year+')'
    else:
        return list_of_author_dict[0]['lastname']+' et al. ('+year+')'

    
def remove_complex_characters_in_string(s):
    s2 = s.translate({ord(x): '' for x in ['\v', '^', '~', '{', '}', '\\', '"', "'", '`']})
    return s2


def build_apa_citation(entry):
    # print(entry)
    if 'number' in entry:
        number_pages = '('+entry['number']+')'
    else:
        number_pages = ''
    if 'pages' in entry:
        number_pages += ' '+entry['pages']
    volume = '}'
    if 'volume' in entry:
        volume = " "+entry['volume']+volume
    return entry['author']+" ("+entry['year']+") \textit{"+entry['journal']+volume+number_pages

def build_library(verbose=False, find_duplicates=False):

    LIBRARY = {}
    abbrevs = []
    for entry in bib_database.entries:
        
        AD = transform_author_to_list_of_dict(entry['author'])
        
        true_abbrev_of_entry = get_abbrev_of_entry(AD, entry, find_duplicates=find_duplicates)
        abbrev_of_entry = remove_complex_characters_in_string(true_abbrev_of_entry)
        true_intext_abbrev_of_entry = get_intext_abbrev_of_entry(AD, entry)
        intext_abbrev_of_entry = remove_complex_characters_in_string(true_intext_abbrev_of_entry)
        
        abbrevs.append(abbrev_of_entry)
        
        try:
            LIBRARY[abbrev_of_entry] = {'correct_abbrev':true_abbrev_of_entry,
                                        'correct_intext_abbrev':true_intext_abbrev_of_entry,
                                        'intext_abbrev':intext_abbrev_of_entry,
                                        'APA':build_apa_citation(entry)}
        except KeyError:
            print('----------------------------------------------------')
            print('problems with entry:')
            print(entry)
        if verbose:
            print(abbrevs[-1])
            
    if find_duplicates:
        return bib_database.entries, np.array(abbrevs)
    else:
        print('----------------------------------------------------')
        print('saving the LIBRARY as "biblio.npz" ')
        np.savez('biblio.npz', **LIBRARY)
    
def find_duplicates(verbose=False):
    """

    """
    entries, abbrevs = build_library(verbose=verbose, find_duplicates=True)
    DUPLICATES = [[] for a in abbrevs] # an emty list of duplicates
    
    uabbrevs, indices, counts = np.unique(abbrevs,
                                    return_counts=True,
                                    return_inverse=True)
    
    dup_abbrevs_cond = (counts > 1)
    if len(uabbrevs[dup_abbrevs_cond])>1:
        for ua in uabbrevs[dup_abbrevs_cond]:
            dup_indices = np.argwhere(ua==abbrevs).flatten()
            if verbose:
                print('conflicting fields for :', ua)
            for ud in dup_indices:
                try:
                    if verbose:
                        print('-->', entries[ud]['ID'],\
                              'becomes ', ua.replace(entries[ud]['year'], entries[ud]['year2']))
                except KeyError:
                    if verbose:
                        print('NEED TO ADD A "year2" ENTRY FOR ',
                              entries[ud]['ID'])
                    
                DUPLICATES[ud] = list(dup_indices)
                DUPLICATES[ud].remove(ud)

    return DUPLICATES

              
# in case not used as a modulus
if __name__=='__main__':


    # s = 'Lind{\'e}n et al., 2011'
    # print(s.replace('{\'e}', 'e'))
    # import argparse
    # parser=argparse.ArgumentParser()
    # args = parser.parse_args()

    if sys.argv[-1]=='build':
        print('[...] creating the library file')
        DUPLICATES = build_library()
    elif sys.argv[-1]=='clean':
        print('[...] clean the biblio.bib file')
        DUPLICATES = find_duplicates(verbose=True)
    elif sys.argv[1]=='check':
        LIBRARY = dict(np.load('biblio.npz'))
        print(LIBRARY[sys.argv[2]])
    else:
        print('--------------------------')
        print(' need ot provide an argument, either:')
        print(' build')
        print(' clean')
        


    

