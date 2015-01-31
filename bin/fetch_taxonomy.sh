# Fields in the DWC occurrence.txt file:
#    $197: datasetid
#    $128: kingdom
#    $165: phylum
#    $67: class
#    $158: order
#    $93: family
#    $100: genus
#    $220: species
grep -v "gbifID" $1 | awk 'BEGIN {FS="\t"} {OFS="\t"} {print $197,$128,$165,$67,$158,$93,$100,$220}' | sort | uniq -c > temp_taxonomy.txt
python src/merge_taxonomy_2icicle.py temp_taxonomy.txt settings.json
#rm temp_taxonomy.txt
