#!/bin/bash
dir=kaon

python kaon/my_analysis.py $dir/roots/no_cuts.root $dir/pdfs/hists/ &
python kaon/my_analysis.py $dir/roots/all_cuts.root  $dir/pdfs/all_cuts/ &

python kaon/brandon.py &

wait
