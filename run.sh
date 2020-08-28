# directory of that file
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

finalyz_script() {
    python $DIR/finalyz/main.py $@
}
alias finalyz=finalyz_script


report_script() {
    python $DIR/finalyz/main.py $1 --report --abstract_key '' --citation_style 'number_exponents' --references_key '' --insert_informations_at_the_end    
}
alias report=report_script


# echo "----------------------------------------------------------------------------------------------"
# echo "If you want to permanently add 'finalyz' to your system"
# echo "  add the following to your bash configuration file (either '~/.profile' or '~/.bash_profile')"
# echo ""
# echo '"""'
# echo "finalyz_script() {"
# echo " python "$DIR"/finalyz/main.py \$@"
# echo "}"
# echo "alias finalyz=finalyz_script"
# echo '"""'

