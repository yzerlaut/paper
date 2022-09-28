mkdir pngs -p
readarray array <<< cut -d ' '  -f 3 <<< $(inkscape --actions="select-all:layers;select-list;" $1)

declare -i count=1
for i in "${array[@]}"
do
  echo $(cut -d ' ' -f 1 <<< $i)
  myLayer=$(cut -d ' ' -f 1 <<< $i)
  $(inkscape --export-area-page --actions="export-id-only;export-id:$myLayer;export-filename:pngs/layer$count.png;export-do;" $1)
  # $(inkscape --export-area-page --actions="export-id-only;export-id:$myLayer;export-filename:pngs/$i-$myLayer.png;export-do;" $1)
  count+=1
  echo $count
done
