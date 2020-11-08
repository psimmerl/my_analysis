#!/bin/bash
dir=/volatile/clas12/psimmerl/my_analysis/kaon

rm $dir/*.root
#rm $dir/kaon_FD_events.hipo
#run-groovy make_hipo.groovy /cache/clas12/rg-a/production/recon/fall2018/torus-1/pass1/v0/dst/train/skim4/*.hipo

run-groovy gen_hist.groovy $dir/kaon_events.hipo $dir/no_cuts.root 
python2.7 kaon/run_brandon_volatile.py $dir/no_cuts.root $dir/hists/

run-groovy gen_hist.groovy $dir/kaon_events.hipo $dir/mass_cuts.root ecut pcut kpcut kmcut &
run-groovy gen_hist.groovy $dir/kaon_events.hipo $dir/vz_cut.root    vzcut &
run-groovy gen_hist.groovy $dir/kaon_events.hipo $dir/cp_cut.root    cpcut &
run-groovy gen_hist.groovy $dir/kaon_events.hipo $dir/ckp_cut.root   ckpcut &
run-groovy gen_hist.groovy $dir/kaon_events.hipo $dir/ckm_cut.root   ckmcut &
run-groovy gen_hist.groovy $dir/kaon_events.hipo $dir/cop_cuts.root  cpcut ckpcut ckmcut &

wait

python2.7 kaon/run_brandon_volatile.py $dir/mass_cuts.root $dir/mass_cuts/
python2.7 kaon/run_brandon_volatile.py $dir/vz_cut.root    $dir/vz_cut/
python2.7 kaon/run_brandon_volatile.py $dir/cp_cut.root    $dir/cp_cut/
python2.7 kaon/run_brandon_volatile.py $dir/ckp_cut.root   $dir/ckp_cut/
python2.7 kaon/run_brandon_volatile.py $dir/ckm_cut.root   $dir/ckm_cut/
python2.7 kaon/run_brandon_volatile.py $dir/cop_cuts.root  $dir/cop_cuts/


