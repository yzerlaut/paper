# Finding the directlry of the script (to point to txt_process.py, see below)
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null && pwd )"

# # ---------- EMACS & ORG-MODE & LATEX working for *.txt files !
# # function for latex compil
# tex_compil_func() {
#     if [ -d "tex/" ]; then echo ""; else mkdir tex/; fi;
#     original_string=$1
#     string_to_put='.tex'
#     if [ ${original_string: -4} == ".txt" ];
#     then tex_file="${original_string/.txt/$string_to_put}"; fi
#     if [ ${original_string: -4} == ".org" ];
#     then tex_file="${original_string/.org/$string_to_put}"; fi
#     if [ -f $tex_file ]; then mv $tex_file tex/; fi;
#     pdflatex -shell-escape -interaction=nonstopmode -output-directory=tex/ tex/$tex_file > tex/compil_output
#     string_to_put='.pdf'
#     pdf_file="${original_string/.tex/$string_to_put}"
#     mv tex/$pdf_file $pdf_file
# }
# bib_compil_func() {
#     cd tex/
#     if [ ! -f biology_citations.bst ]; then cp ~/work/common_libraries/tex/biology_citations.bst ./; fi;
#     if [ ! -f biology_citations.sty ]; then cp ~/work/common_libraries/tex/biology_citations.sty ./; fi;
#     original_string=$1
#     string_to_put='.aux'
#     if [ ${original_string: -4} == ".txt" ];
#     then aux_file="${original_string/.txt/$string_to_put}"; fi
#     if [ ${original_string: -4} == ".org" ];
#     then aux_file="${original_string/.org/$string_to_put}"; fi
#     # aux_file="${original_string/.org/$string_to_put}"
#     bibtex -terse $aux_file
#     cd ..
# }

# # PRESENTATION
# pres_func() {
#     emacs --batch -l $HOME/work/common_libraries/org-mode/org-config-pres.el --file $1 -f org-beamer-export-to-latex
#     tex_compil_func $1
# }
# alias pres=pres_func

# PAPER
paper_func() {
    python $DIR/txt_process.py $@
    # python $DIR/txt_process.py $txt_file
    # python $HOME/work/common_libraries/tex/from_paper_txt_to_tex.py $@
    # tex_extent="tex"
    # tex_file="${txt_file/txt/tex}"
    # tex_compil_func $tex_file
    # emacs --batch -l $HOME/work/common_libraries/org-mode/org-config-paper.el --file $1 -f org-latex-export-to-latex
    # tex_compil_func $1; bib_compil_func $1; tex_compil_func $1
}
alias paper=paper_func

# # REPORT
# report_func() {
#     emacs --batch -l $HOME/work/common_libraries/org-mode/org-config-report.el --file $1 -f org-latex-export-to-latex
#     tex_compil_func $1; bib_compil_func $1; tex_compil_func $1
# }
# alias report=report_func

# # SUPPLEMENTARY
# report_func() {
#     emacs --batch -l $HOME/work/common_libraries/org-mode/org-config-supp.el --file $1 -f org-latex-export-to-latex
#     tex_compil_func $1; bib_compil_func $1; tex_compil_func $1
# }
# alias supp=supp_func
# alias latex_clean_up='rm *.out;rm *.snm;rm *.toc;rm *.log;rm *.aux;rm *.out'

# # ORG to DOCX
# org2docx() {
#       pandoc --bibliography=tex/biblio.bib --csl=$HOME/work/common_libraries/tex/jneurophysiol.csl -i $1 -o $1-pandoc.docx
#   }
