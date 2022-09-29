layers2png() {

    readarray array <<< cut -d ' '  -f 3 <<< $(inkscape --actions="select-all:layers;select-list;" $1)

    declare -i count=1

    for i in "${array[@]}"
    do
      echo $(cut -d ' ' -f 1 <<< $i)
      myLayer=$(cut -d ' ' -f 1 <<< $i)
      $(inkscape --export-area-page --actions="export-id-only;export-id:$myLayer;export-filename:$2-layer$count.png;export-do;" $1)
      count+=1
      # echo $count
    done

}

echo 'loaded layers2png [...]'
