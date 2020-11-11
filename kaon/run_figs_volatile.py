import ROOT, math, sys, argparse
from MyHist import * 

pDir  = "~/my_analysis/kaon/pdfs/"

ct = "counts"
xvz = "#Delta Vz_{K^{+}}-Vz_{K^{-}}"
xim2, yim2 = "I.M. PrK^{-}", "I.M. K^{+}K^{-}"
im,xim = ["improkp","improkm","imkpkm"],["I.M. PrK^{+}","I.M. PrK^{-}","I.M. K^{+}K^{-}"]
xc = ["Coplanarity "+s for s in ["#Theta_{pr}","#Theta_{K^{+}}","#Theta_{K^{-}}"]]
ep,MM=": ep#rightarrow e","Missing Mass"

cg, cb = "PASS_","FAIL_"

f32t = "/volatile/clas12/psimmerl/my_analysis/kaon/no_cuts.root"
f32c = "/volatile/clas12/psimmerl/my_analysis/kaon/mass_cuts.root"

met   = MyHist(cg+"me",    f32t, "Missing Energy"+ep+"pK^{+}K^{-}X", "Energy (GeV)", ct, "mm")
mep   = MyHist(cg+"me",    f32c, "Missing Energy"+ep+"pK^{+}K^{-}X", "Energy (GeV)", ct, "mm")
mef   = MyHist(cb+"me",    f32c, "Missing Energy"+ep+"pK^{+}K^{-}X", "Energy (GeV)", ct, "mm")

prot  = MyHist(cg+"mmpro", f32t, MM+ep+"K^{+}K^{-}X", "Proton Mass (GeV)", ct, "mm")
prop  = MyHist(cg+"mmpro", f32c, MM+ep+"k^{+}K^{-}X", "Proton Mass (GeV)", ct, "mm")
prof  = MyHist(cb+"mmpro", f32c, MM+ep+"K^{+}K^{-}X", "Proton Mass (GeV)", ct, "mm")

kpt   = MyHist(cg+"mm2kp", f32t, MM+"^{2}"+ep+"pK^{-}X", "K^{+} Mass^{2} (GeV^{2})", ct, "mm")
kpp   = MyHist(cg+"mm2kp", f32c, MM+"^{2}"+ep+"pK^{-}X", "K^{+} Mass^{2} (GeV^{2})", ct, "mm")
kpf   = MyHist(cb+"mm2kp", f32c, MM+"^{2}"+ep+"pK^{-}X", "K^{+} Mass^{2} (GeV^{2})", ct, "mm")

kmt   = MyHist(cg+"mm2km", f32t, MM+"^{2}"+ep+"pK^{+}X", "K^{-} Mass^{2} (GeV^{2})", ct, "mm")
kmp   = MyHist(cg+"mm2km", f32c, MM+"^{2}"+ep+"pK^{+}X", "K^{-} Mass^{2} (GeV^{2})", ct, "mm")
kmf   = MyHist(cb+"mm2km", f32c, MM+"^{2}"+ep+"pK^{+}X", "K^{-} Mass^{2} (GeV^{2})", ct, "mm")
    
im2 = MyHist(cg+"im2D", f32c, "(FD), "+yim2+" vs "+xim2+", Pass All Cuts", \
                  xim2+" (GeV)", yim2+" (GeV)","im2D")

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
    
h37p = MyHist(cg+im[1], f36, "(FD), "+xim[1]+", Pass All,--<I.M.k^{+}K^{-}<--",\
                  xim[1]+" (GeV)", ct,"imk")
    
h38p = MyHist(cg+im[2], f36, "Invariant Mass of Charged Kaons from epK^{+}K^{-}", xim[2]+" (GeV)",\
                ct,"imk")
    
    
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
met.Draw( "same",pDir+"32b.pdf",1)
mep.Draw( "same",pDir+"32b.pdf",1)
mef.Draw( "same",pDir+"32b.pdf",1)

prot.Draw("same",pDir+"32b.pdf",2)
prop.Draw("same",pDir+"32b.pdf",2)
prof.Draw("same",pDir+"32b.pdf",2)

kpt.Draw( "same",pDir+"32b.pdf",4)
kpp.Draw( "same",pDir+"32b.pdf",4)
kpf.Draw( "same",pDir+"32b.pdf",4)

kmt.Draw( "same",pDir+"32b.pdf",3)
kmp.Draw( "same",pDir+"32b.pdf",3)
kmf.Draw( "same",pDir+"32b.pdf",3)

im2.setCanvas(True); im2.Draw("COLZ", pDir+"33.pdf")

vz.setCanvas(True); vz.Draw("", pDir+"34a.pdf")

h34br.setCanvas(True) 
h34br.Draw( "same",pDir+"34b.pdf")
h34bp.Draw( "same",pDir+"34b.pdf")
h34bf.Draw( "same",pDir+"34b.pdf")


cp.setCanvas(True); cp.Draw( "",pDir+"35a.pdf")
ckp.setCanvas(True); ckp.Draw( "",pDir+"35c.pdf")
ckm.setCanvas(True); ckm.Draw( "",pDir+"35e.pdf")

h35bt.setCanvas(True)
h35bt.Draw("same",pDir+"35b.pdf")
h35bp.Draw("same",pDir+"35b.pdf")
h35bf.Draw("same",pDir+"35b.pdf")

h35dt.setCanvas(True)
h35dt.Draw("same",pDir+"35d.pdf")
h35dp.Draw("same",pDir+"35d.pdf")
h35df.Draw("same",pDir+"35d.pdf")

h35ft.setCanvas(True)
h35ft.Draw("same",pDir+"35f.pdf")
h35fp.Draw("same",pDir+"35f.pdf")
h35ff.Draw("same",pDir+"35f.pdf")

h36r.setCanvas(True)
h36r.Draw("same",pDir+"36.pdf")
h36p.Draw("same",pDir+"36.pdf")
h36f.Draw("same",pDir+"36.pdf")

h37p.setCanvas(True); h37p.Draw("",pDir+"37.pdf")
h38p.setCanvas(True); h38p.Draw("",pDir+"38.pdf")


