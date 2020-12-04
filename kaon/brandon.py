import ROOT, math, sys, argparse
from MyHist import MyHist

pDir = "kaon/pdfs/"
iDir = "kaon/roots/"#"/volatile/clas12/psimmerl/my_analysis/kaon/"

ct = "counts"
xvz = "#Delta Vz_{K^{+}}-Vz_{K^{-}}"
xim2, yim2 = "I.M. PrK^{-}", "I.M. K^{+}K^{-}"
im,xim = ["improkp","improkm","imkpkm"],["I.M. PrK^{+}","I.M. PrK^{-}","I.M. K^{+}K^{-}"]
xc = ["Coplanarity "+s for s in ["#Theta_{pr}","#Theta_{K^{+}}","#Theta_{K^{-}}"]]
ep,MM2=": ep#rightarrow e","Missing Mass^{2}"

cg, cb = "PASS_","FAIL_"

f32t = iDir+"no_cuts_inb.root"
f32c = iDir+"mass_cuts_inb.root"

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
    

f34c=iDir+"mass_vz_cuts_inb.root"
vz  = MyHist(cg+"dvz", f32c, "(FD), "+xvz+"Pass", xvz+" (cm)", ct,"dvz")
h34br= MyHist(cg+im[2], f32c, xim[2]+" Pass-Fail "+xvz, xim[2]+" (GeV)", ct,"imk")
h34bp= MyHist(cg+im[2], f34c, xim[2]+" Pass-Fail "+xvz, xim[2]+" (GeV)", ct,"imk")
h34bf= MyHist(cb+im[2], f34c, xim[2]+" Pass-Fail "+xvz, xim[2]+" (GeV)", ct,"imk")
    
f35bc=iDir+"mass_vz_cp_cuts_inb.root"
f35dc=iDir+"mass_vz_ckp_cuts_inb.root"
f35fc=iDir+"mass_vz_ckm_cuts_inb.root"
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
    
f36=iDir+"mass_vz_cop_cuts_inb.root"
h36r= MyHist(cg+im[2], f34c, xim[2]+", Pass-Fail All Coplan. Cuts", xim[2]+" (GeV)", ct,"imk")
h36p= MyHist(cg+im[2], f36, xim[2]+", Pass-Fail All Coplan. Cuts", xim[2]+" (GeV)", ct,"imk")
h36f= MyHist(cb+im[2], f36, xim[2]+", Pass-Fail All Coplan. Cuts", xim[2]+" (GeV)", ct,"imk")
    

im2 = MyHist(cg+"im2D", f36, "(FD), "+yim2+" vs "+xim2+", Pass All Cuts", \
                  xim2+" (GeV)", yim2+" (GeV)","im2D")

f37i = iDir+"mass_vz_cop_ikk_cuts_inb.root"
f37o = iDir+"mass_vz_cop_ikk_cuts_outb.root"
h37i = MyHist(cg+im[1], f37i, "(FD) inbNoutb, "+xim[1]+", Pass All,--<I.M.K^{+}K^{-}<--",\
                  xim[1]+" (GeV)", ct,"imk")
h37o = MyHist(cg+im[1], f37o, "(FD) outb, "+xim[1]+", Pass All,--<I.M.K^{+}K^{-}<--",\
                  xim[1]+" (GeV)", ct,"imk")
h37i.Add(h37o)

    
h38p = MyHist(cg+im[2], f36, "Invariant Mass of Charged Kaons from epK^{+}K^{-}", xim[2]+" (GeV)",\
                ct,"imk")


met.setRange(  [-1.5,1.5] );mep.setRange(  [-1.5,1.5] );mef.setRange(  [-1.5,1.5] )
prot.setRange( [0,2] );prop.setRange( [0,2] );prof.setRange( [0,2] )
kpt.setRange( [-.5,1.5] );kpp.setRange( [-.5,1.5] );kpf.setRange( [-.5,1.5] )
kmt.setRange( [-.5,1.5] );kmp.setRange( [-.5,1.5] );kmf.setRange( [-.5,1.5] )

met.setCanvas(True,2,2)
met.Draw( "same",pDir+"32b.png",1,ROOT.kBlack,print_fit=False)
mep.Draw( "same",pDir+"32b.png",1,ROOT.kBlue,print_fit=False)
mef.Draw( "same",pDir+"32b.png",1,ROOT.kRed,print_fit=False)

prot.Draw("same",pDir+"32b.png",2,ROOT.kBlack,print_fit=False)
prop.Draw("same",pDir+"32b.png",2,ROOT.kBlue,print_fit=False)
prof.Draw("same",pDir+"32b.png",2,ROOT.kRed,print_fit=False)

kpt.Draw( "same",pDir+"32b.png",4,ROOT.kBlack,print_fit=False)
kpp.Draw( "same",pDir+"32b.png",4,ROOT.kBlue,print_fit=False)
kpf.Draw( "same",pDir+"32b.png",4,ROOT.kRed,print_fit=False)

kmt.Draw( "same",pDir+"32b.png",3,ROOT.kBlack,print_fit=False)
kmp.Draw( "same",pDir+"32b.png",3,ROOT.kBlue,print_fit=False)
kmf.Draw( "same",pDir+"32b.png",3,ROOT.kRed,print_fit=False)

ppars=prot.gaussFit( 0.938 )
mepars=met.gaussFit( 0.0 )
kppars=kpt.gaussFit( 0.494**2 )
kmpars=kmt.gaussFit( 0.494**2 )

met.setRange(  [-1.5,1.5] );mep.setRange(  [-1.5,1.5] );mef.setRange(  [-1.5,1.5] )
prot.setRange( [0,2] );prop.setRange( [0,2] );prof.setRange( [0,2] )
kpt.setRange( [-.5,1.5] );kpp.setRange( [-.5,1.5] );kpf.setRange( [-.5,1.5] )
kmt.setRange( [-.5,1.5] );kmp.setRange( [-.5,1.5] );kmf.setRange( [-.5,1.5] )

met.setCanvas(True,2,2)
met.Draw( "same",pDir+"32a.png",1, lines=[mepars[1]+4*mepars[2],mepars[1]-4*mepars[2]])
prot.Draw("same",pDir+"32a.png",2, lines=[ppars[1]+4*ppars[2],ppars[1]-4*ppars[2]])
kpt.Draw( "same",pDir+"32a.png",4, lines=[kppars[1]+4*kppars[2],kppars[1]-4*kppars[2]])
kmt.Draw( "same",pDir+"32a.png",3, lines=[kmpars[1]+4*kmpars[2],kmpars[1]-4*kmpars[2]])

im2.setCanvas(True); im2.Draw("COLZ", pDir+"33.png")

vzpars = vz.gaussFit( 0.0 )
vz.setCanvas(True);
vz.Draw("same", pDir+"34a.png",lines=[vzpars[1]+4*vzpars[2],vzpars[1]-4*vzpars[2]])

h34br.setCanvas(True,1,1) 
h34br.Draw( "same",pDir+"34b.png",1,ROOT.kBlack)
h34bp.Draw( "same",pDir+"34b.png",1,ROOT.kBlue)
h34bf.Draw( "same",pDir+"34b.png",1,ROOT.kRed)


cp.setCanvas(True); cp.Draw( "",pDir+"35a.png",lines=[9])
ckp.setCanvas(True); ckp.Draw( "",pDir+"35c.png",lines=[9])
ckm.setCanvas(True); ckm.Draw( "",pDir+"35e.png",lines=[9])

h35bt.setCanvas(True)
h35bt.Draw("same",pDir+"35b.png",1,ROOT.kBlack)
h35bp.Draw("same",pDir+"35b.png",1,ROOT.kBlue)
h35bf.Draw("same",pDir+"35b.png",1,ROOT.kRed)

h35dt.setCanvas(True)
h35dt.Draw("same",pDir+"35d.png",1,ROOT.kBlack)
h35dp.Draw("same",pDir+"35d.png",1,ROOT.kBlue)
h35df.Draw("same",pDir+"35d.png",1,ROOT.kRed)

h35ft.setCanvas(True)
h35ft.Draw("same",pDir+"35f.png",1,ROOT.kBlack)
h35fp.Draw("same",pDir+"35f.png",1,ROOT.kBlue)
h35ff.Draw("same",pDir+"35f.png",1,ROOT.kRed)

h36r.setCanvas(True)
h36r.Draw("same",pDir+"36.png",1,ROOT.kBlack)
h36p.Draw("same",pDir+"36.png",1,ROOT.kBlue)
h36f.Draw("same",pDir+"36.png",1,ROOT.kRed)

h37i.setCanvas(True); h37i.Draw("",pDir+"37.png")
h38p.gaussFit( 1.02 )
h38p.setRange([0.96,1.14])
h38p.setCanvas(True); h38p.Draw("",pDir+"38.png")



