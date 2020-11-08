package clas12.mon.paul

import org.jlab.clas.physics.LorentzVector
import org.jlab.groot.data.H1F
import org.jlab.groot.data.H2F
import java.util.concurrent.ConcurrentHashMap
import uconn.utils.pid.stefan.ElectronCandidate
import uconn.utils.pid.stefan.PionCandidate
import uconn.utils.pid.stefan.ElectronCandidate.Cut
import uconn.utils.pid.stefan.PionCandidate.Cut
import my.Sugar
import utils.KinTool
import groovy.json.JsonSlurper

class cut_EPPipPim_mon {
  def hists = new ConcurrentHashMap()

  def beam = LorentzVector.withPID(11,0,0,10.6)
  def target = LorentzVector.withPID(2212,0,0,0)

  def ele_cuts = null
  def pip_cuts = null
  def pim_cuts = null
  def mm2_fit_data = {}
  
  def mm2 = true
  def phase = true
  def q2w = true
  def masspro = true
  def masspip = true
  def masspim = true

  def name = ""

  def hmm2 = {new H1F("$it","$it",250,-0.5,2)}
  def him = {new H1F("$it","$it",180,0.2,2)}

  def hThetaP = {new H2F("$it", "$it", 1000, 0, 90, 1000, 0, 10)}
  def hPhiP = {new H2F("$it", "$it", 1000, -30, 330, 1000, 0, 10)}
  def hThetaPhi = {new H2F("$it", "$it", 1000, 0, 90, 1000, -30, 330)}

  def hW2D = {new H2F("$it", "$it", 1000, 0, 4.5, 1000, 0, 10)}
  
  def banknames = ['RUN::config', 'REC::Particle','REC::Calorimeter','REC::Cherenkov','REC::Traj']
  
  def cut_EPPipPim_mon(name='',ele_cuts=null,pip_cuts=null,pim_cuts=null,mm2=true,phase=true,q2w=true,masspro=false,masspip=false,masspim=false) {
    setCuts(ele_cuts, pip_cuts, pim_cuts)
    setHists(mm2, phase, q2w, masspro, masspip, masspim)
    setName(name)
  }

  def setCuts(ele_cuts=null, pip_cuts=null, pim_cuts=null) {
    this.ele_cuts=ele_cuts
    this.pip_cuts=pip_cuts
    this.pim_cuts=pim_cuts
  }

  def setHists(mm2 = true, phase = true, q2w=true, masspro=true, masspip=true, masspim=true) {
    this.mm2 = mm2
    this.phase = phase
    this.q2w = q2w
    this.masspro = masspro
    this.masspip = masspip
    this.masspim = masspim
    if ( masspro || masspip || masspim ) {
      def slurper = new JsonSlurper()
      this.mm2_fit_data = new ConcurrentHashMap(slurper.parse(new File('/volatile/clas12/psimmerl/my_analysis/pion/mm2_fits_no_mass_cut.json')))
    }
  }

  def setName(name='') {
    this.name = name
  }
  
  def processEvent(event) {
    if(banknames.every{event.hasBank(it)}) {
      def (runb, partb,calb, ccb, trajb) = banknames.collect{event.getBank(it)}

      (0..<partb.rows()).findAll{partb.getInt('pid',it)==11 && partb.getShort("status",it)<0}
        .collectMany{iele->
          (0..<partb.rows()).findAll{partb.getInt('pid',it)==2212}.collect{ipro->[iele,ipro]}
        }.collectMany{iele,ipro->
          (0..<partb.rows()).findAll{partb.getInt('pid',it)==211}.collect{ipip->[iele,ipro,ipip]}
        }.collectMany{iele,ipro,ipip->
          (0..<partb.rows()).findAll{partb.getInt('pid',it)==-211}.collect{ipim->[iele,ipro,ipip,ipim]}
        }.each{iele,ipro,ipip,ipim->
          def ele = LorentzVector.withPID(11,*['px','py','pz'].collect{partb.getFloat(it,iele)})
          def pro = LorentzVector.withPID(2212,*['px','py','pz'].collect{partb.getFloat(it,ipro)})
          def pip = LorentzVector.withPID(211,*['px','py','pz'].collect{partb.getFloat(it,ipip)})
          def pim = LorentzVector.withPID(-211,*['px','py','pz'].collect{partb.getFloat(it,ipim)})
          def sec = calb.getByte('sector',iele)
          
          def mm2pip = beam+target-ele-pro-pim
          def mm2pim = beam+target-ele-pro-pip
          def mm2pro = beam+target-ele-pip-pim

          def prodet = (partb.getShort('status',ipro)/1000/1).toInteger()==2 ? 'FD':'CD'
          def pipdet = (partb.getShort('status',ipip)/1000/1).toInteger()==2 ? 'FD':'CD'
          def pimdet = (partb.getShort('status',ipim)/1000/1).toInteger()==2 ? 'FD':'CD'
          def detname = "pro_${prodet}_pip_${pipdet}_pim_${pimdet}"

          def ele_cand = ElectronCandidate.getElectronCandidate(iele, partb, calb, ccb, trajb)
          def pip_cand = PionCandidate.getPionCandidate(ipip, partb, trajb)
          def pim_cand = PionCandidate.getPionCandidate(ipim, partb, trajb)
          
          def isgood = true
          if (ele_cuts.size()>0) { isgood = ele_cand.iselectron(*ele_cuts) }
          if (pip_cuts.size()>0 && isgood) { isgood = pip_cand.ispip(*pip_cuts) }
          if (pim_cuts.size()>0 && isgood) { isgood = pim_cand.ispim(*pim_cuts) }
          
          if ( (masspro || masspip || masspim) && isgood ) {
            def hname = "($name GOOD,"
            if ( prodet == 'FD' && pipdet == 'FD' && pimdet == 'FD'){ hname = "$hname ALL FD)" }
            else if( prodet == 'CD' && pipdet == 'CD' && pimdet == 'CD' ){ hname = "$hname ALL CD)" }
            else { hname = "$hname only ${prodet=='FD'?'p':''}${pipdet=='FD'?'pi+':''}"+
                        "${pimdet=='FD'?'pi-':''} FD)" }
            /*println("\"Missing Mass (GeV) pro $hname\"")
            println(mm2_fit_data["Missing Mass (GeV) pro $hname"])
            println(mm2_fit_data["Missing Mass (GeV) pro $hname"][3])
            println(mm2_fit_data["Missing Mass (GeV) pro $hname"][3][1])
            */def mu0pro  = mm2_fit_data["Missing Mass (GeV) pro $hname"][3][1]
            def sig0pro = mm2_fit_data["Missing Mass (GeV) pro $hname"][3][2]
            def mu0pip  = mm2_fit_data["Missing Mass Squared (GeV^2) pip $hname"][3][1]
            def sig0pip = mm2_fit_data["Missing Mass Squared (GeV^2) pip $hname"][3][2]
            def mu0pim  = mm2_fit_data["Missing Mass Squared (GeV^2) pim $hname"][3][1]
            def sig0pim = mm2_fit_data["Missing Mass Squared (GeV^2) pim $hname"][3][2]
            //println("----")
            
					  if (masspro == true && isgood) { isgood = Math.abs((mm2pro.mass()-mu0pro)/sig0pro/1)<3 }
					  if (masspip == true && isgood) { isgood = Math.abs((mm2pip.mass2()-mu0pip)/sig0pip/1)<3 }
					  if (masspim == true && isgood) { isgood = Math.abs((mm2pim.mass2()-mu0pim)/sig0pim/1)<3 }
				  }	
					
          def gbname = name+(isgood ? '_GOOD':'_BAD')

          if ( mm2 ) {
            hists.computeIfAbsent("${gbname}_mmpro_$detname", hmm2).fill(mm2pro.mass())
            hists.computeIfAbsent("${gbname}_mm2pip_$detname",hmm2).fill(mm2pip.mass2())
            hists.computeIfAbsent("${gbname}_mm2pim_$detname",hmm2).fill(mm2pim.mass2())
          }
          if ( phase ) {
            def (px,py,pz) = ['px','py','pz'].collect{partb.getFloat(it,iele)}
            def theta = Math.asin(Math.sqrt(px**2+py**2)/pz)*180/Math.PI
            def phi = Math.atan2(py,px)*180/Math.PI/1
            //def adj_phi = phi-(((sec-1)*60-(sec>4 ? 1 : 0))+(sec==4 ? 1 : 0)*(phi<0 ? 1 : 0))*360
            def adj_phi = phi+360*(phi<-30 ? 1 : 0)
            hists.computeIfAbsent("${gbname}_H2F_sec${sec}_ThetaP",hThetaP).fill(theta, ele.p())
            hists.computeIfAbsent("${gbname}_H2F_PhiP",hPhiP).fill(adj_phi, ele.p())
            hists.computeIfAbsent("${gbname}_H2F_ThetaPhi",hThetaPhi).fill(theta, adj_phi)
          }
          if ( q2w ) {
            def Q2 = KinTool.calcQ2(beam, ele)
            def eX  = beam+target-ele   
            hists.computeIfAbsent("${gbname}_H2F_sec${sec}_q2w",hW2D).fill(eX.mass(), Q2)
          }
        }
    }
  }
}
