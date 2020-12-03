#!/bin/bash
dir=kaon

python kaon/run_brandon_volatile.py $dir/roots/no_cuts.root $dir/pdfs/hists/ &
python kaon/run_brandon_volatile.py $dir/roots/all_cuts.root  $dir/pdfs/all_cuts/ &

python kaon/run_figs_volatile.py &

wait

#cp $dir/hists/PASS/*P*         kaon/pdfs/diagnostics/no_cuts/
#cp $dir/hists/PASS/q2w.pdf     kaon/pdfs/diagnostics/no_cuts/
#cp $dir/hists/PASS/q2Xb.pdf    kaon/pdfs/diagnostics/no_cuts/
#cp $dir/all_cuts/PASS/*P*      kaon/pdfs/diagnostics/all_cuts/
#cp $dir/all_cuts/PASS/q2Xb.pdf kaon/pdfs/diagnostics/all_cuts/

