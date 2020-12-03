#!/bin/bash
hdir=/volatile/clas12/psimmerl/my_analysis/kaon
rdir=kaon/roots
pdir=kaon/pdfs
#kFD=$hdir/kaon_FD_events.hipo #My events from skim4 requires epk+km
kFD=/volatile/clas12/kenjo/bclary/phi_skim #Brandons events

rm $rdir/*.root
#rm $dir/kaon_FD_events.hipo
#run-groovy make_hipo.groovy /cache/clas12/rg-a/production/recon/fall2018/torus-1/pass1/v0/dst/train/skim4/*.hipo

run-groovy gen_hist.groovy $kFD $rdir/no_cuts.root $pdir/hists/fits.json
python2.7 kaon/my_analysis.py $rdir/no_cuts.root $pdir/hists/


#My analysis
run-groovy gen_hist.groovy $kFD $rdir/mass_cuts.root $pdir/hists/fits.json ecut pcut kpcut kmcut &
run-groovy gen_hist.groovy $kFD $rdir/vz_cut.root    $pdir/hists/fits.json vzcut &
run-groovy gen_hist.groovy $kFD $rdir/cp_cut.root    $pdir/hists/fits.json cpcut &
run-groovy gen_hist.groovy $kFD $rdir/ckp_cut.root   $pdir/hists/fits.json ckpcut &
run-groovy gen_hist.groovy $kFD $rdir/ckm_cut.root   $pdir/hists/fits.json ckmcut &
run-groovy gen_hist.groovy $kFD $rdir/cop_cuts.root  $pdir/hists/fits.json cpcut ckpcut ckmcut &
run-groovy gen_hist.groovy $kFD $rdir/ikk_cuts.root  $pdir/hists/fits.json ikk &
run-groovy gen_hist.groovy $kFD $rdir/all_cuts.root  $pdir/hists/fits.json ecut pcut kpcut kmcut vzcut cpcut ckpcut ckmcut ikk &

wait

python2.7 kaon/my_analysis.py $rdir/mass_cuts.root $pdir/mass_cuts/ &

wait

python2.7 kaon/my_analysis.py $rdir/vz_cut.root    $pdir/vz_cut/ &
python2.7 kaon/my_analysis.py $rdir/cp_cut.root    $pdir/cp_cut/ &
python2.7 kaon/my_analysis.py $rdir/ckp_cut.root   $pdir/ckp_cut/ &
python2.7 kaon/my_analysis.py $rdir/ckm_cut.root   $pdir/ckm_cut/ &
python2.7 kaon/my_analysis.py $rdir/cop_cuts.root  $pdir/cop_cuts/ &
python2.7 kaon/my_analysis.py $rdir/ikk_cuts.root  $pdir/ikk_cuts/ &
python2.7 kaon/my_analysis.py $rdir/all_cuts.root  $pdir/all_cuts/ &


#Brandon Figs
mcut=$pdir/mass_cuts/fits.json
run-groovy gen_hist.groovy $kFD $rdir/mass_vz_cuts.root     $mcut vz ecut pcut kpcut kmcut vzcut &
run-groovy gen_hist.groovy $kFD $rdir/mass_vz_cp_cuts.root  $mcut cp ecut pcut kpcut kmcut vzcut cpcut &
run-groovy gen_hist.groovy $kFD $rdir/mass_vz_ckp_cuts.root $mcut ckp ecut pcut kpcut kmcut vzcut ckpcut &
run-groovy gen_hist.groovy $kFD $rdir/mass_vz_ckm_cuts.root $mcut ckm ecut pcut kpcut kmcut vzcut ckmcut &
run-groovy gen_hist.groovy $kFD $rdir/mass_vz_cop_cuts.root $mcut cop ecut pcut kpcut kmcut vzcut cpcut ckpcut ckmcut &

wait 
#Should make new hipo based on previous for this next cut so I don't double cut mm2!
python2.7 kaon/my_analysis.py $rdir/mass_vz_cop_cuts.root $pdir/mass_vz_cop_cuts/ 
run-groovy gen_hist.groovy $kFD $rdir/mass_vz_cop_ikk_cuts.root $pdir/mass_vz_cop_cuts/fits.json ikk ecut pcut kpcut kmcut vzcut cpcut ckpcut ckmcut ikkcut

wait

python2.7 kaon/brandon.py 


