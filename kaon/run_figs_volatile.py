import ROOT, math, sys, argparse
from MyHist import * 

pDir  = "/u/home/psimmerl/my_analysis/kaon/pdfs/"

ct = "counts"
xvz = "#Delta Vz_{K^{+}}-Vz_{K^{-}}"
xim2, yim2 = "I.M. PrK^{-}", "I.M. K^{+}K^{-}"
im,xim = ["improkp","improkm","imkpkm"],["I.M. PrK^{+}","I.M. PrK^{-}","I.M. K^{+}K^{-}"]
xc = ["Coplanarity "+s for s in ["#Theta_{pr}","#Theta_{K^{+}}","#Theta_{K^{-}}"]]
ep,MM2=": ep#rightarrow e","Missing Mass^{2}"

cg, cb = "PASS_","FAIL_"

f32t = "/volatile/clas12/psimmerl/my_analysis/kaon/no_cuts.root"
f32c = "/volatile/clas12/psimmerl/my_analysis/kaon/mass_cuts.root"

met   = MyHist(cg+"me",    f32t, "Missing Energy"+ep+"pK^{+}K^{-}X", "Energy (GeV)", ct, "mm")
mep   = MyHist(cg+"me",    f32c, "Missing Energy"+ep+"pK^{+}K^{-}X", "Energy (GeV)", ct, "mm")
mef   = MyHist(cb+"me",    f32c, "Missing Energy"+ep+"pK^{+}K^{-}X", "Energy (GeV)", ct, "mm")

prot  = MyHist(cg+"mm2pro", f32t, MM2+ep+"K^{+}K^{-}X", "Proton Mass (GeV^{2})", ct, "mm")
prop  = MyHist(cg+"mm2pro", f32c, MM2+ep+"k^{+}K^{-}X", "Proton Mass (GeV^{2})", ct, "mm")
prof  = MyHist(cb+"mm2pro", f32c, MM2+ep+"K^{+}K^{-}X", "Proton Mass (GeV^{2})", ct, "mm")

kpt   = MyHist(cg+"mm2kp", f32t, MM2+ep+"pK^{-}X", "K^{+} Mass (GeV^{2})", ct, "mm")
kpp   = MyHist(cg+"mm2kp", f32c, MM2+ep+"pK^{-}X", "K^{+} Mass (GeV^{2})", ct, "mm")
kpf   = MyHist(cb+"mm2kp", f32c, MM2+ep+"pK^{-}X", "K^{+} Mass (GeV^{2})", ct, "mm")

kmt   = MyHist(cg+"mm2km", f32t, MM2+ep+"pK^{+}X", "K^{-} Mass (GeV^{2})", ct, "mm")
kmp   = MyHist(cg+"mm2km", f32c, MM2+ep+"pK^{+}X", "K^{-} Mass (GeV^{2})", ct, "mm")
kmf   = MyHist(cb+"mm2km", f32c, MM2+ep+"pK^{+}X", "K^{-} Mass (GeV^{2})", ct, "mm")
    

f34c="/volatile/clas12/psimmerl/my_analysis/kaon/mass_vz_cuts.root"
vz  = MyHist(cg+"dvz", f32c, "(FD), "+xvz+"Pass", xvz+" (cm)", ct,"dvz")
h34br= MyHist(cg+im[2], f32c, xim[2]+" Pass-Fail "+xvz, xim[2]+" (GeV)", ct,"imk")
h34bp= MyHist(cg+im[2], f34c, xim[2]+" Pass-Fail "+xvz, xim[2]+" (GeV)", ct,"imk")
h34bf= MyHist(cb+im[2], f34c, xim[2]+" Pass-Fail "+xvz, xim[2]+" (GeV)", ct,"imk")
    
f35bc="/volatile/clas12/psimmerl/my_analysis/kaon/mass_vz_cp_cuts.root"
f35dc="/volatile/clas12/psimmerl/my_analysis/kaon/mass_vz_ckp_cuts.root"
f35fc="/volatile/clas12/psimmerl/my_analysis/kaon/mass_vz_ckm_cuts.root"
pac, pfc, l9 = ", Pass All Cuts", xim[2]+", Pass-Fail Coplan. #theta_{","<9 deg Cuts"
cp = MyHist(cg+"coplanepro",f34c, "Proton (FD), "+xc[0]+pac, xc[0], ct,"coplane")
h35bt= MyHist(cg+im[2], f34c, pfc+"pr}"+l9, xim[2]+" (GeV)",           ct,"imk")
h35bp= MyHist(cg+im[2], f35bc, pfc+"pr}"+l9, xim[2]+" (GeV)",           ct,"imk")
h35bf= MyHist(cb+im[2], f35bc, pfc+"pr}"+l9, xim[2]+" (GeV)",           ct,"imk")
ckp = MyHist(cg+"coplanekp", f34c, "K^{+} (FD), "+xc[1]+pac, xc[1], ct,"coplane")
h35dt= MyHist(cg+im[2], f34c, pfc+"K^{+}}"+l9, xim[2]+" (GeV)",           ct,"imk")
h35dp= MyHist(cg+im[2], f35dc, pfc+"K^{+}}"+l9, xim[2]+" (GeV)",           ct,"imk")
h35df= MyHist(cb+im[2], f35dc, pfc+"K^{+}}"+l9, xim[2]+" (GeV)",           ct,"imk")
ckm = MyHist(cg+"coplanekm", f34c, "K^{-} (FD), "+xc[2]+pac, xc[2], ct,"coplane")
h35ft= MyHist(cg+im[2], f34c, pfc+"K^{-}}"+l9, xim[2]+" (GeV)",           ct,"imk")
h35fp= MyHist(cg+im[2], f35fc, pfc+"K^{-}}"+l9, xim[2]+" (GeV)",           ct,"imk")
h35ff= MyHist(cb+im[2], f35fc, pfc+"K^{-}}"+l9, xim[2]+" (GeV)",           ct,"imk")
    
f36="/volatile/clas12/psimmerl/my_analysis/kaon/mass_vz_cop_cuts.root"
h36r= MyHist(cg+im[2], f34c, xim[2]+", Pass-Fail All Coplan. Cuts", xim[2]+" (GeV)", ct,"imk")
h36p= MyHist(cg+im[2], f36, xim[2]+", Pass-Fail All Coplan. Cuts", xim[2]+" (GeV)", ct,"imk")
h36f= MyHist(cb+im[2], f36, xim[2]+", Pass-Fail All Coplan. Cuts", xim[2]+" (GeV)", ct,"imk")
    
f37 = "/volatile/clas12/psimmerl/my_analysis/kaon/mass_vz_cop_ikk_cuts.root"
im2 = MyHist(cg+"im2D", f36, "(FD), "+yim2+" vs "+xim2+", Pass All Cuts", \
                  xim2+" (GeV)", yim2+" (GeV)","im2D")

h37p = MyHist(cg+im[1], f37, "(FD), "+xim[1]+", Pass All,--<I.M.K^{+}K^{-}<--",\
                  xim[1]+" (GeV)", ct,"imk")
    
h38p = MyHist(cg+im[2], f36, "Invariant Mass of Charged Kaons from epK^{+}K^{-}", xim[2]+" (GeV)",\
                ct,"imk")

    
    
prot.gaussFit( 0.938 )
met.gaussFit( 0.0 )
kpt.gaussFit( 0.494**2 )
kmt.gaussFit( 0.494**2 )

met.setRange(  [-1.5,1.5] )
mep.setRange(  [-1.5,1.5] )
mef.setRange(  [-1.5,1.5] )

prot.setRange( [0,2] )
prop.setRange( [0,2] )
prof.setRange( [0,2] )

kpt.setRange( [-.5,1.5] )
kpp.setRange( [-.5,1.5] )
kpf.setRange( [-.5,1.5] )

kmt.setRange( [-.5,1.5] )
kmp.setRange( [-.5,1.5] )
kmf.setRange( [-.5,1.5] )
      


met.setCanvas(True,2,2)
met.Draw( "same",pDir+"32a.pdf",1)
prot.Draw("same",pDir+"32a.pdf",2)
kpt.Draw( "same",pDir+"32a.pdf",4)
kmt.Draw( "same",pDir+"32a.pdf",3)

met.setCanvas(True,2,2)
met.Draw( "same",pDir+"32b.pdf",1,ROOT.kBlack)
mep.Draw( "same",pDir+"32b.pdf",1,ROOT.kBlue)
mef.Draw( "same",pDir+"32b.pdf",1,ROOT.kRed)

prot.Draw("same",pDir+"32b.pdf",2,ROOT.kBlack)
prop.Draw("same",pDir+"32b.pdf",2,ROOT.kBlue)
prof.Draw("same",pDir+"32b.pdf",2,ROOT.kRed)

kpt.Draw( "same",pDir+"32b.pdf",4,ROOT.kBlack)
kpp.Draw( "same",pDir+"32b.pdf",4,ROOT.kBlue)
kpf.Draw( "same",pDir+"32b.pdf",4,ROOT.kRed)

kmt.Draw( "same",pDir+"32b.pdf",3,ROOT.kBlack)
kmp.Draw( "same",pDir+"32b.pdf",3,ROOT.kBlue)
kmf.Draw( "same",pDir+"32b.pdf",3,ROOT.kRed)

im2.setCanvas(True); im2.Draw("COLZ", pDir+"33.pdf")

vz.gaussFit( 0.0 )
vz.setCanvas(True); vz.Draw("", pDir+"34a.pdf")

h34br.setCanvas(True,1,1) 
h34br.Draw( "same",pDir+"34b.pdf",1,ROOT.kBlack)
h34bp.Draw( "same",pDir+"34b.pdf",1,ROOT.kBlue)
h34bf.Draw( "same",pDir+"34b.pdf",1,ROOT.kRed)


cp.setCanvas(True); cp.Draw( "",pDir+"35a.pdf")
ckp.setCanvas(True); ckp.Draw( "",pDir+"35c.pdf")
ckm.setCanvas(True); ckm.Draw( "",pDir+"35e.pdf")

h35bt.setCanvas(True)
h35bt.Draw("same",pDir+"35b.pdf",1,ROOT.kBlack)
h35bp.Draw("same",pDir+"35b.pdf",1,ROOT.kBlue)
h35bf.Draw("same",pDir+"35b.pdf",1,ROOT.kRed)

h35dt.setCanvas(True)
h35dt.Draw("same",pDir+"35d.pdf",1,ROOT.kBlack)
h35dp.Draw("same",pDir+"35d.pdf",1,ROOT.kBlue)
h35df.Draw("same",pDir+"35d.pdf",1,ROOT.kRed)

h35ft.setCanvas(True)
h35ft.Draw("same",pDir+"35f.pdf",1,ROOT.kBlack)
h35fp.Draw("same",pDir+"35f.pdf",1,ROOT.kBlue)
h35ff.Draw("same",pDir+"35f.pdf",1,ROOT.kRed)

h36r.setCanvas(True)
h36r.Draw("same",pDir+"36.pdf",1,ROOT.kBlack)
h36p.Draw("same",pDir+"36.pdf",1,ROOT.kBlue)
h36f.Draw("same",pDir+"36.pdf",1,ROOT.kRed)

h37p.setCanvas(True); h37p.Draw("",pDir+"37.pdf")
h38p.gaussFit( 1.02 )
h38p.setRange([0.96,1.14])
h38p.setCanvas(True); h38p.Draw("",pDir+"38.pdf")



