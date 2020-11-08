import ROOT, math, sys, argparse
from MyHist import * 

if len(sys.argv) > 1:
  ff    = sys.argv[1] #"/volatile/clas12/psimmerl/my_analysis/kaon/hists.root"
  #fjson = sys.argv[2] #"/volatile/clas12/psimmerl/my_analysis/kaon/mm2_fits.json"
  pDir  = sys.argv[2] #"/volatile/clas12/psimmerl/my_analysis/kaon/hists/"
  #cuts  = sys.argv[4:]
else:
  ff    = "/volatile/clas12/psimmerl/my_analysis/kaon/hists.root"
  #fjson = "/volatile/clas12/psimmerl/my_analysis/kaon/mm2_fits.json"
  pDir  = "/volatile/clas12/psimmerl/my_analysis/kaon/hists/"
#  cuts  = ["FD"]
fjson = pDir+"fits.json"
for cut in ["FD"]:#cuts:
  for gb in ["PASS"]:#,"FAIL"]:
    c_gb,cgb,ct = gb+"_", " ("+gb+")","counts"
    fdir = pDir+gb+"/"
    xvz = "#Delta Vz_{K^{+}}-Vz_{K^{-}}"
    xim2, yim2 = "I.M. PrK^{-}", "I.M. K^{+}K^{-}"
    im,xim = ["improkp","improkm","imkpkm"],["I.M. PrK^{+}","I.M. PrK^{-}","I.M. K^{+}K^{-}"]
    xc = ["Coplanarity "+s for s in ["#Theta_{pr}","#Theta_{K^{+}}","#Theta_{K^{-}}"]]
    me   = MyHist(c_gb+"me",        ff, "Missing Energy"+cgb,   "Energy (GeV)",             ct, "mm")
    mm   = MyHist(c_gb+"mm",        ff, "Missing Mass"+cgb,     "Mass (GeV)",               ct, "mm")
    pro  = MyHist(c_gb+"mmpro",     ff, "Missing Mass"  +cgb,   "Proton Mass (GeV)",        ct, "mm")
    kp   = MyHist(c_gb+"mm2kp",     ff, "Missing Mass^{2}"+cgb, "K^{+} Mass^{2} (GeV^{2})", ct, "mm")
    km   = MyHist(c_gb+"mm2km",     ff, "Missing Mass^{2}"+cgb, "K^{-} Mass^{2} (GeV^{2})", ct, "mm")
    vz   = MyHist(c_gb+"dvz",       ff, xvz+cgb,                 xvz+" (cm)",               ct,"dvz")
    ipkp = MyHist(c_gb+im[0],       ff, xim[0]+cgb,              xim[0]+" (GeV)",           ct,"imk")
    ipkm = MyHist(c_gb+im[1],       ff, xim[1]+cgb,              xim[1]+" (GeV)",           ct,"imk")
    ikpkm= MyHist(c_gb+im[2],       ff, xim[2]+cgb,              xim[2]+" (GeV)",           ct,"imk")
    cp   = MyHist(c_gb+"coplanepro",ff, "Proton, "+xc[0]+cgb,    xc[0],                 ct,"coplane")
    ckp  = MyHist(c_gb+"coplanekp", ff, "K^{+}, "+xc[1]+cgb,     xc[1],                 ct,"coplane")
    ckm  = MyHist(c_gb+"coplanekm", ff, "K^{-}, "+xc[2]+cgb,     xc[2],                 ct,"coplane")
    im2  = MyHist(c_gb+"im2D",      ff, yim2+" vs "+xim2+cgb,    xim2+" (GeV)", yim2+" (GeV)","im2D")
    q2w  = MyHist(c_gb+"q2w",       ff, "Q^{2} vs W"+cgb,       "W (GeV)",  "Q^{2} (GeV^{2})", "q2w")
    ThP,PhiP,ThPhi =[],[],[]
    for p, P in zip(["ele","pro","kp","km"],[s+", "for s in ["Electron","Proton","K^{+}","K^{-}"]]):
      ThP.append(  MyHist(c_gb+p+"_ThP",  ff, P+"P  vs #Theta"+cgb,  "#Theta","P (GeV)","ThP"))
      PhiP.append( MyHist(c_gb+p+"_PhiP", ff, P+"P vs #Phi"+cgb,     "#Phi",  "P (GeV)","PhiP"))
      ThPhi.append(MyHist(c_gb+p+"_ThPhi",ff, P+"#Phi vs #Theta"+cgb,"#Theta","#Phi",   "ThPhi"))
    me.getJsonFile(fjson)
    
    if gb == "PASS":
      me.gaussFit( 0.0 )
      mm.gaussFit( 0.0 )
      pro.gaussFit( 0.938 )
      kp.gaussFit( 0.494**2 )
      km.gaussFit( 0.494**2 )
      vz.gaussFit( 0.0 )
    me.setRange(  [-1.5,1.5] )
    pro.setRange( [0,2] )
    kp.setRange( [-.5,1.5] )
    km.setRange( [-.5,1.5] )
      
    mm.setCanvas(True); mm.Draw("", fdir+"mm.pdf")
    pro.setCanvas(True,2,2)
    me.Draw( "same",fdir+"mmm.pdf",1)
    pro.Draw("same",fdir+"mmm.pdf",2)
    kp.Draw( "same",fdir+"mmm.pdf",4)
    km.Draw( "same",fdir+"mmm.pdf",3)
    vz.setCanvas(True); vz.Draw("", fdir+"dvz.pdf")
    ipkp.setCanvas(True,3,1)
    ipkp.Draw( "same",fdir+"im.pdf",1)
    ipkm.Draw( "same",fdir+"im.pdf",2)
    ikpkm.Draw("same",fdir+"im.pdf",3)
    cp.setCanvas(True,3,1)
    cp.Draw( "same",fdir+"coplane.pdf",1)
    ckp.Draw("same",fdir+"coplane.pdf",2)
    ckm.Draw("same",fdir+"coplane.pdf",3)
    im2.setCanvas(True); im2.Draw("COLZ", fdir+"im2D.pdf")
    q2w.setCanvas(True); q2w.Draw("COLZ", fdir+"q2w.pdf")
    ThP[0].setCanvas(  True,2,2); 
    for i in range(4): ThP[i].Draw(  "COLZ", fdir+"ThetaP.pdf",  i+1)
    PhiP[0].setCanvas( True,2,2); 
    for i in range(4): PhiP[i].Draw( "COLZ", fdir+"PhiP.pdf",    i+1)
    ThPhi[0].setCanvas(True,2,2); 
    for i in range(4): ThPhi[i].Draw("COLZ", fdir+"ThetaPhi.pdf",i+1)
    
    os.system("pdfunite "+fdir+"* "+"~/my_analysis/kaon/pdfs/"+\
            "_".join(fdir.split("/")[-3:-1])+".pdf")

    #w    = [q2w.ProjectionX(c_gb+"w_q2bin"+str(q2), BinFloor(q2, bc),BinFloor(q2+1,bc)) for q2 in range(10)]
    #W
