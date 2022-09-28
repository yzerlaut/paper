readarray array <<< cut -d ' '  -f 3 <<< $(inkscape --actions="select-all:layers;select-list;" $1)

for i in "${array[@]}"
do
  echo $(cut -d ' ' -f 1 <<< $i)
  myLayer=$(cut -d ' ' -f 1 <<< $i)
  $(inkscape --export-area-page --actions="export-id-only;export-id:$myLayer;export-filename:$myLayer.png;export-do;" $1)
done
