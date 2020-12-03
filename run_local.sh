#!/bin/bash
dir=kaon

python kaon/my_analysis.py $dir/roots/no_cuts_inb.root $dir/pdfs/hists_inb/ &
python kaon/my_analysis.py $dir/roots/all_cuts_inb.root  $dir/pdfs/all_cuts_inb/ &

python kaon/brandon.py &

wait
