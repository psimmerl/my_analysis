import math, ROOT, os
from array import array
import json

ROOT.gROOT.SetBatch()
#ROOT.gStyle.SetEndErrorSize(10)
ROOT.gStyle.SetOptFit()
ROOT.gStyle.SetPadGridX(ROOT.kTRUE)
ROOT.gStyle.SetPadGridY(ROOT.kTRUE)
ROOT.gStyle.SetOptStat("")


class MyData:
  templates = { "mm"       : ROOT.TH1F("mm",      "mm",      250, -1.5, 2),   \
                "impro"    : ROOT.TH1F("impro",   "impro",   180, 1.3,  3.0), \
                "imk"      : ROOT.TH1F("imk",     "imk",     180, 0.95, 1.5), \
                "dvz"      : ROOT.TH1F("dvz",     "dvz",     250, -20,  20),  \
                "coplane"  : ROOT.TH1F("coplane", "coplane", 250, 0,    10),  \
                "ThP"      : ROOT.TH2F("ThP",   "ThP",   1000, 0,   90,  1000, 0,   10),  \
                "PhiP"     : ROOT.TH2F("PhiP",  "PhiP",  1000, -30, 330, 1000, 0,   10),  \
                "ThPhi"    : ROOT.TH2F("ThPhi", "ThPhi", 1000, 0,   90,  1000, -30, 330), \
                "im2D"     : ROOT.TH2F("im2D",  "im2D",  180,  0.5, 5,   180,  0.8, 2.2), \
                "q2w"      : ROOT.TH2F("q2w",   "q2w",   1000, 0,   4.5, 1000, 0,   10) }
  #linewidth = 2
  c = ROOT.TCanvas("c","c",800,800)
  fjson = {"json_name" : ""}
  froot = ROOT.TFile()

class MyHist(MyData):
  def __init__(self, name, fname, title="", xlabel="x", ylabel="y", template="mm2" ):
    self.name = name
    self.setRootFile(fname)
    self.getHist(name, template)
    self.setLabels(title, xlabel, ylabel)
    self.fitted = False

  def setLabels(self, title, xlabel, ylabel ):
    self.hist.SetTitle(title)
    self.hist.GetXaxis().SetTitle(xlabel)
    self.hist.GetYaxis().SetTitle(ylabel)

  def setRootFile(self, fname ):
    self.froot =  ROOT.TFile( fname )
   
  def GetName(self):
    return self.name

  def getJsonFile(self, fname ):
    self.fjson["json_name"] = fname
    try:
      with open(fname) as f:
        self.fjson.update(json.load(f))
    except:
      print("JSON not found")
      if not os.path.isdir("/".join(fname.split("/")[0:-1])):
        os.makedirs("/".join(fname.split("/")[0:-1]))
      with open(fname,"w") as f:
        json.dump(self.fjson, f)
        
  def Add(self, *hists):
    for h in hists:
      self.hist.Add(h.hist) 

  def gaussFit(self, mu0, dmu0=0.4 ):
    if self.hist.GetEntries() == 0:
      print("Can't Fit!")
      self.fjson[self.name] = [0, [0, mu0, 5*mu0, 0, 0, 0]] 
      return None

    xa = self.hist.GetXaxis()
    ya = self.hist.GetYaxis()
    xmin,xmax=xa.GetXmin(),xa.GetXmax()
    self.setRange([mu0-dmu0,mu0+dmu0])
    A0, mu0_b = self.hist.GetMaximum(), self.hist.GetMaximumBin()
    mu0 = self.hist.GetBinCenter(mu0_b)
    sig0, k = 0, 0
    for i in range(-8, 0)+range(1, 9): 
      bv = self.hist.GetBinContent(mu0_b+i)
      bc = self.hist.GetBinCenter(mu0_b+i)
      if bv > 0 and bv < A0: 
        sig0 += math.sqrt(-(mu0-bc)**2/(2*math.log(bv/A0)))
        k+=1
    if sig0 == 0:
      sig0 = 0.05
    else:
      sig0 = sig0/k
    xlow, xhigh = mu0-3*sig0, mu0+3*sig0
    self.setRange([xlow, xhigh])
    p1 = (self.hist.GetBinContent(xa.FindBin(xhigh))-self.hist.GetBinContent(xa.FindBin(xlow)))\
          /(xhigh-xlow)
    p0 = self.hist.GetBinContent(xa.FindBin(xlow))-p1*xlow
    A0_2 = A0-p0-p1*mu0 
    pars = [A0_2, mu0, sig0, p0, p1, 0] 

    self.fit = ROOT.TF1(self.hist.GetTitle()+"_fit", "gaus(0)+pol"+str(len(pars[3:])-1)+"(3)", \
                xlow, xhigh)
    self.gaus = ROOT.TF1(self.hist.GetTitle()+"_gaus", "gaus(0)", xlow, xhigh)
    self.bg = ROOT.TF1(self.hist.GetTitle()+"_poly", "pol"+str(len(pars[3:])-1)+"(0)", xlow, xhigh)
    self.lg = ROOT.TLegend(.6,.59,1,.9)
    self.lg.SetTextFont(72)
    self.lg.SetTextSize(0.04)#hist.SetStats(0)
    
    self.fit.SetParameters(*pars)
    self.fit.SetParNames("A", "\mu", "\sigma", "Cons", "Lin", "Quad")
    for i in range(len(pars)):
      if pars[i] != 0:
        self.fit.SetParLimits(i, *sorted([pars[i]*.25, pars[i]*1.75]))
      elif i>3:
        self.fit.SetParLimits(i, *sorted([-1*abs(pars[i-1]*.25), abs(pars[i]*.25)]))
    
    for i in range(2):
      self.hist.Fit(self.fit, "QRM0")
      pars, errs = self.fit.GetParameters(), self.fit.GetParErrors()
      self.setRange([pars[1]-3*pars[2], pars[1]+3*pars[2]])
    
    self.gaus.SetParameters(pars[0],pars[1],pars[2])
    self.bg.SetParameters(pars[3],pars[4],pars[5])
    
    self.fit.SetRange(pars[1]-3*pars[2], pars[1]+3*pars[2])
    self.gaus.SetRange(pars[1]-3*pars[2], pars[1]+3*pars[2])
    self.bg.SetRange(pars[1]-3*pars[2], pars[1]+3*pars[2])
    
    #lg.AddEntry(None, "\mu {:.5f}".format(pars[1]), "")#
    #lg.AddEntry(None, " \pm{:.5f} GeV".format(errs[1]), "")
    #lg.AddEntry(None, "\sigma {:.5f}".format(pars[2]), "")
    #lg.AddEntry(None, " \pm{:.5f} GeV".format(errs[2]), "")
    #lg.AddEntry(None, "\Chi^{2}"+"/NDF {:.1e}".format(fit.GetChisquare()/((xhigh-xlow)*100-len(pars))) ,"")#fit.GetNDF(),4)),"")
    
    self.lg.AddEntry(self.fit, "Global Fit", "")
    self.lg.AddEntry(self.fit, "Gaussian Fit", "")
    self.lg.AddEntry(self.fit, "Background Fit", "")
    
    self.setRange([xmin,xmax])
    self.fjson[self.name] = [self.hist.GetEntries(),\
          [pars[0],pars[1],pars[2],pars[3],pars[4],pars[5]]]
    self.fitted = True
    return self.fit.GetParameters()
    
  def getFitPars(self):
    return self.hist.GetParameters()  

  def setRange(self, x=None, y=None ):
    xa = self.hist.GetXaxis()
    ya = self.hist.GetYaxis()
    if x is not None: xa.SetRange(xa.FindBin(x[0]), xa.FindBin(x[1]))
    if y is not None: ya.SetRange(ya.FindBin(y[0]), ya.FindBin(y[1]))

  def getHist(self, name, template ):
    if name in self.froot.GetListOfKeys(): 
      self.hist = self.froot.Get(name)
    else:
      print("Could not find "+name)
      self.hist = self.templates[template].Clone()
      self.hist.SetName(name)

  def zoom3Sigma(self):
    pars = self.fit.GetParameters()
    setRange([pars[1]-3*pars[2], pars[1]+3*pars[2]])

  def setCanvas(self, clear=False, rows=1, cols=1):
    if clear:
      self.c.Clear()
    self.c.Divide(cols,rows)

  def Draw(self, drawopt, fname, pos = 1, col=ROOT.kBlue, print_bg=True ):
    self.c.cd(pos)
    if self.hist.__class__ is ROOT.TH1F:
      self.hist.SetMinimum(0)
    self.hist.SetLineColor(col)
    self.hist.Draw(drawopt)
    
    if print_bg and self.fitted:
      ROOT.gStyle.SetOptStat("e")
      #self.lg.Draw("same")
      self.fit.Draw("same");self.fit.SetLineColor(ROOT.kRed)
      self.gaus.Draw("same");self.gaus.SetLineColor(ROOT.kMagenta)
      self.bg.Draw("same");self.bg.SetLineColor(ROOT.kGreen)
    else:
      ROOT.gStyle.SetOptStat("")
    
    if self.fjson["json_name"] != "":
      with open(self.fjson["json_name"], 'w') as f:
        json.dump(self.fjson, f)
    
    if not os.path.isdir("/".join(fname.split("/")[0:-1])):
      os.makedirs("/".join(fname.split("/")[0:-1]))
    self.c.Print(fname)
  
