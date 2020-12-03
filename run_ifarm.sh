#!/bin/bash
hdir=/volatile/clas12/psimmerl/my_analysis/kaon
rdir=kaon/roots
pdir=kaon/pdfs
#kFD=$hdir/kaon_FD_events.hipo #My events from skim4 requires epk+km
kFDi=/volatile/clas12/kenjo/bclary/phi_skim/inb/skim8_*.hipo #Brandons inb events
kFDo=/volatile/clas12/kenjo/bclary/phi_skim/outb/epKpKm_RGA_OUT.hipo #Brandons outb events


rm $rdir/*.root
#rm $dir/kaon_FD_events.hipo
#run-groovy make_hipo.groovy /cache/clas12/rg-a/production/recon/fall2018/torus-1/pass1/v0/dst/train/skim4/*.hipo


run-groovy gen_hist.groovy $kFDi $rdir/no_cuts_inb.root $pdir/hists_inb/fits.json all 
run-groovy gen_hist.groovy $kFDo $rdir/no_cuts_outb.root $pdir/hists_outb/fits.json all 

wait
python2.7 kaon/my_analysis.py $rdir/no_cuts_inb.root $pdir/hists_inb/
python2.7 kaon/my_analysis.py $rdir/no_cuts_outb.root $pdir/hists_outb/

wait


#My analysis
run-groovy gen_hist.groovy $kFDi $rdir/mass_cuts_inb.root $pdir/hists_inb/fits.json all ecut pcut kpcut kmcut &
run-groovy gen_hist.groovy $kFDi $rdir/vz_cut_inb.root    $pdir/hists_inb/fits.json all vzcut &
run-groovy gen_hist.groovy $kFDi $rdir/cp_cut_inb.root    $pdir/hists_inb/fits.json all cpcut &
run-groovy gen_hist.groovy $kFDi $rdir/ckp_cut_inb.root   $pdir/hists_inb/fits.json all ckpcut &
run-groovy gen_hist.groovy $kFDi $rdir/ckm_cut_inb.root   $pdir/hists_inb/fits.json all ckmcut &
run-groovy gen_hist.groovy $kFDi $rdir/cop_cuts_inb.root  $pdir/hists_inb/fits.json all cpcut ckpcut ckmcut &
run-groovy gen_hist.groovy $kFDi $rdir/ikk_cuts_inb.root  $pdir/hists_inb/fits.json all ikk &
run-groovy gen_hist.groovy $kFDi $rdir/all_cuts_inb.root  $pdir/hists_inb/fits.json all ecut pcut kpcut kmcut vzcut cpcut ckpcut ckmcut ikk &

run-groovy gen_hist.groovy $kFDo $rdir/mass_cuts_outb.root $pdir/hists_outb/fits.json all ecut pcut kpcut kmcut &
run-groovy gen_hist.groovy $kFDo $rdir/vz_cut_outb.root    $pdir/hists_outb/fits.json all vzcut &
run-groovy gen_hist.groovy $kFDo $rdir/cp_cut_outb.root    $pdir/hists_outb/fits.json all cpcut &
run-groovy gen_hist.groovy $kFDo $rdir/ckp_cut_outb.root   $pdir/hists_outb/fits.json all ckpcut &
run-groovy gen_hist.groovy $kFDo $rdir/ckm_cut_outb.root   $pdir/hists_outb/fits.json all ckmcut &
run-groovy gen_hist.groovy $kFDo $rdir/cop_cuts_outb.root  $pdir/hists_outb/fits.json all cpcut ckpcut ckmcut &
run-groovy gen_hist.groovy $kFDo $rdir/ikk_cuts_outb.root  $pdir/hists_outb/fits.json all ikk &
run-groovy gen_hist.groovy $kFDo $rdir/all_cuts_outb.root  $pdir/hists_outb/fits.json all ecut pcut kpcut kmcut vzcut cpcut ckpcut ckmcut ikk &

wait

python2.7 kaon/my_analysis.py $rdir/mass_cuts_inb.root $pdir/mass_cuts_inb/ &
python2.7 kaon/my_analysis.py $rdir/mass_cuts_outb.root $pdir/mass_cuts_outb/ &


wait

python2.7 kaon/my_analysis.py $rdir/vz_cut_inb.root    $pdir/vz_cut_inb/ &
python2.7 kaon/my_analysis.py $rdir/cp_cut_inb.root    $pdir/cp_cut_inb/ &
python2.7 kaon/my_analysis.py $rdir/ckp_cut_inb.root   $pdir/ckp_cut_inb/ &
python2.7 kaon/my_analysis.py $rdir/ckm_cut_inb.root   $pdir/ckm_cut_inb/ &
python2.7 kaon/my_analysis.py $rdir/cop_cuts_inb.root  $pdir/cop_cuts_inb/ &
python2.7 kaon/my_analysis.py $rdir/ikk_cuts_inb.root  $pdir/ikk_cuts_inb/ &
python2.7 kaon/my_analysis.py $rdir/all_cuts_inb.root  $pdir/all_cuts_inb/ &

python2.7 kaon/my_analysis.py $rdir/vz_cut_outb.root    $pdir/vz_cut_outb/ &
python2.7 kaon/my_analysis.py $rdir/cp_cut_outb.root    $pdir/cp_cut_outb/ &
python2.7 kaon/my_analysis.py $rdir/ckp_cut_outb.root   $pdir/ckp_cut_outb/ &
python2.7 kaon/my_analysis.py $rdir/ckm_cut_outb.root   $pdir/ckm_cut_outb/ &
python2.7 kaon/my_analysis.py $rdir/cop_cuts_outb.root  $pdir/cop_cuts_outb/ &
python2.7 kaon/my_analysis.py $rdir/ikk_cuts_outb.root  $pdir/ikk_cuts_outb/ &
python2.7 kaon/my_analysis.py $rdir/all_cuts_outb.root  $pdir/all_cuts_outb/ &


#Brandon Figs
mcuti=$pdir/mass_cuts_inb/fits.json
mcuto=$pdir/mass_cuts_outb/fits.json
run-groovy gen_hist.groovy $kFDi $rdir/mass_vz_cuts_inb.root     $mcuti vz ecut pcut kpcut kmcut vzcut &
run-groovy gen_hist.groovy $kFDi $rdir/mass_vz_cp_cuts_inb.root  $mcuti cp ecut pcut kpcut kmcut vzcut cpcut &
run-groovy gen_hist.groovy $kFDi $rdir/mass_vz_ckp_cuts_inb.root $mcuti ckp ecut pcut kpcut kmcut vzcut ckpcut &
run-groovy gen_hist.groovy $kFDi $rdir/mass_vz_ckm_cuts_inb.root $mcuti ckm ecut pcut kpcut kmcut vzcut ckmcut &
run-groovy gen_hist.groovy $kFDi $rdir/mass_vz_cop_cuts_inb.root $mcuti cop ecut pcut kpcut kmcut vzcut cpcut ckpcut ckmcut &

run-groovy gen_hist.groovy $kFDo $rdir/mass_vz_cuts_outb.root     $mcuto vz ecut pcut kpcut kmcut vzcut &
run-groovy gen_hist.groovy $kFDo $rdir/mass_vz_cp_cuts_outb.root  $mcuto cp ecut pcut kpcut kmcut vzcut cpcut &
run-groovy gen_hist.groovy $kFDo $rdir/mass_vz_ckp_cuts_outb.root $mcuto ckp ecut pcut kpcut kmcut vzcut ckpcut &
run-groovy gen_hist.groovy $kFDo $rdir/mass_vz_ckm_cuts_outb.root $mcuto ckm ecut pcut kpcut kmcut vzcut ckmcut &
run-groovy gen_hist.groovy $kFDo $rdir/mass_vz_cop_cuts_outb.root $mcuto cop ecut pcut kpcut kmcut vzcut cpcut ckpcut ckmcut &


wait 
#Should make new hipo based on previous for this next cut so I don't double cut mm2!
python2.7 kaon/my_analysis.py $rdir/mass_vz_cop_cuts_inb.root $pdir/mass_vz_cop_cuts_inb/ 
python2.7 kaon/my_analysis.py $rdir/mass_vz_cop_cuts_outb.root $pdir/mass_vz_cop_cuts_outb/ 

wait

run-groovy gen_hist.groovy $kFDi $rdir/mass_vz_cop_ikk_cuts_inb.root $pdir/mass_vz_cop_ikk_cuts_inb/fits.json ikk ecut pcut kpcut kmcut vzcut cpcut ckpcut ckmcut ikkcut
run-groovy gen_hist.groovy $kFDo $rdir/mass_vz_cop_ikk_cuts_outb.root $pdir/mass_vz_cop_ikk_cuts_outb/fits.json ikk ecut pcut kpcut kmcut vzcut cpcut ckpcut ckmcut ikkcut


wait

python2.7 kaon/brandon.py 


