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

class EPKpKm_FD_mon {
  def hists = new ConcurrentHashMap()

  def beam = LorentzVector.withPID(11,0,0,10.6)
  def target = LorentzVector.withPID(2212,0,0,0)

  def mm2_fit_data = new ConcurrentHashMap()

  def pcut   = true
  def kpcut  = true
  def kmcut  = true
  def ecut   = true
  def vzcut  = true
  def cpcut  = true
  def ckpcut = true
  def ckmcut = true

  def name = ""

  def hmm2 = {new H1F("$it","$it",350,-1.5,2)}
  
  def himpro = {new H1F("$it","$it",180,1.3,3.0)}
  def himk = {new H1F("$it","$it",180,0.95,1.5)}
  def him2D = {new H2F("$it","$it",250,0.5,5, 250, 0.8, 2.2)}
  def hvz = {new H1F("$it","$it",250,-20,20)}
  def hcoplane = {new H1F("$it","$it",250,0,10)}

  def hThetaP = {new H2F("$it", "$it", 1000, 0, 90, 1000, 0, 10)}
  def hPhiP = {new H2F("$it", "$it", 1000, -30, 330, 1000, 0, 10)}
  def hThetaPhi = {new H2F("$it", "$it", 1000, 0, 90, 1000, -30, 330)}

  def hW2D = {new H2F("$it", "$it", 1000, 0, 4.5, 1000, 0, 10)}
  
  def banknames = ['RUN::config', 'REC::Particle','REC::Calorimeter','REC::Cherenkov','REC::Traj']
  
  def EPKpKm_FD_mon(ecut=false,pcut=false,kpcut=false,kmcut=false,vzcut=false,cpcut=false,ckpcut=false,ckmcut=false) {
    this.pcut   = pcut
    this.kpcut  = kpcut
    this.kmcut  = kmcut
    this.ecut   = ecut
    this.vzcut  = vzcut
    this.cpcut  = cpcut
    this.ckpcut = ckpcut
    this.ckmcut = ckmcut
    if ( pcut || kpcut || kmcut || ecut || vzcut || cpcut || ckpcut || ckmcut ) {
      def slurper = new JsonSlurper()
      this.mm2_fit_data = new ConcurrentHashMap(slurper.parse(new File('/volatile/clas12/psimmerl/my_analysis/kaon/hists/fits.json')))
    }
  }

  def processEvent(event) {
    if(banknames.every{event.hasBank(it)}) {
      def (runb, partb,calb, ccb, trajb) = banknames.collect{event.getBank(it)}

      (0..<partb.rows()).findAll{partb.getInt('pid',it)==11 && partb.getShort("status",it)<0}
        .collectMany{iele->
          (0..<partb.rows()).findAll{partb.getInt('pid',it)==2212}.collect{ipro->[iele,ipro]}
        }.collectMany{iele,ipro->
          (0..<partb.rows()).findAll{partb.getInt('pid',it)==321}.collect{ikp->[iele,ipro,ikp]}
        }.collectMany{iele,ipro,ikp->
          (0..<partb.rows()).findAll{partb.getInt('pid',it)==-321}.collect{ikm->[iele,ipro,ikp,ikm]}
        }.each{iele,ipro,ikp,ikm->
          def ele = LorentzVector.withPID(11,*['px','py','pz'].collect{partb.getFloat(it,iele)})
          def pro = LorentzVector.withPID(2212,*['px','py','pz'].collect{partb.getFloat(it,ipro)})
          def kp = LorentzVector.withPID(321,*['px','py','pz'].collect{partb.getFloat(it,ikp)})
          def km = LorentzVector.withPID(-321,*['px','py','pz'].collect{partb.getFloat(it,ikm)})
          def sec = calb.getByte('sector',iele)
          
          def mm2kp = beam+target-ele-pro-km
          def mm2km = beam+target-ele-pro-kp
          def mm2pro = beam+target-ele-kp-km
          def mm = beam+target-ele-pro-kp-km
          def improkp = pro+kp
          def improkm = pro+km
          def imkpkm  = kp+km
          
          def eX  = beam+target-ele   
          def Q2 = KinTool.calcQ2(beam, ele)
          
          def vzkp = partb.getFloat('vz', ikp) 
          def vzkm = partb.getFloat('vz', ikm)
          
          def pd = (partb.getShort('status',ipro)/1000/1).toInteger()==2
          def kpd = (partb.getShort('status',ikp)/1000/1).toInteger()==2
          def kmd = (partb.getShort('status',ikm)/1000/1).toInteger()==2
          def isgood = pd && kpd && kmd
          if (!isgood) { /*println("Uh oh");*/ return null }

          if ( (ecut || pcut || kpcut || kmcut || vzcut || cpcut || ckpcut || ckmcut) && isgood ) {
            def mu0pro  = mm2_fit_data["PASS_mmpro"][1][1]
            def sig0pro = mm2_fit_data["PASS_mmpro"][1][2]
            def mu0kp   = mm2_fit_data["PASS_mm2kp"][1][1]
            def sig0kp  = mm2_fit_data["PASS_mm2kp"][1][2]
            def mu0km   = mm2_fit_data["PASS_mm2km"][1][1]
            def sig0km  = mm2_fit_data["PASS_mm2km"][1][2]
            def mu0me   = mm2_fit_data["PASS_me"][1][1]
            def sig0me  = mm2_fit_data["PASS_me"][1][2]
            def mu0vz   = mm2_fit_data["PASS_dvz"][1][1]
            def sig0vz  = mm2_fit_data["PASS_dvz"][1][2]
            if ( pcut   ) { isgood = isgood && Math.abs((mm2pro.mass()-mu0pro)/sig0pro/1) < 4 }
            if ( kpcut  ) { isgood = isgood && Math.abs((mm2kp.mass2()-mu0kp)/sig0kp/1) < 4 }
            if ( kmcut  ) { isgood = isgood && Math.abs((mm2km.mass2()-mu0km)/sig0km/1) < 4 }
            if ( ecut   ) { isgood = isgood && Math.abs((mm.e()-mu0me)/sig0me/1) < 4 }
            if ( vzcut  ) { isgood = isgood && ((vzkp-vzkm)-mu0vz)/sig0vz/1 < 4 }
            if ( cpcut  ) { isgood = isgood && mm2pro.vect().theta(pro.vect()) < 9 }
            if ( ckpcut ) { isgood = isgood && mm2kp.vect().theta(kp.vect()) < 9 }
            if ( ckmcut ) { isgood = isgood && mm2km.vect().theta(km.vect()) < 9 }

          }

          def gbname = (isgood ? 'PASS':'FAIL')

          hists.computeIfAbsent("${gbname}_me",hmm2).fill(mm.e())
          hists.computeIfAbsent("${gbname}_mm",hmm2).fill(mm.mass())
          hists.computeIfAbsent("${gbname}_mmpro",hmm2).fill(mm2pro.mass())
          hists.computeIfAbsent("${gbname}_mm2kp",hmm2).fill(mm2kp.mass2())
          hists.computeIfAbsent("${gbname}_mm2km",hmm2).fill(mm2km.mass2())
          
          hists.computeIfAbsent("${gbname}_improkp",himpro).fill(improkp.mass())
          hists.computeIfAbsent("${gbname}_improkm",himpro).fill(improkm.mass())
          hists.computeIfAbsent("${gbname}_imkpkm",himk).fill(imkpkm.mass())
          hists.computeIfAbsent("${gbname}_im2D",him2D).fill(improkm.mass(), imkpkm.mass())
          
          
          hists.computeIfAbsent("${gbname}_dvz",hvz).fill(vzkp-vzkm)
          hists.computeIfAbsent("${gbname}_coplanepro",hcoplane).fill(mm2pro.vect().theta(pro.vect()))
          hists.computeIfAbsent("${gbname}_coplanekp",hcoplane).fill(mm2kp.vect().theta(kp.vect()))
          hists.computeIfAbsent("${gbname}_coplanekm",hcoplane).fill(mm2km.vect().theta(km.vect())) 
          
          hists.computeIfAbsent("${gbname}_q2w",hW2D).fill(eX.mass(), Q2)
          
          [[iele,ele,"ele"],[ipro,pro,"pro"],[ikp,kp,"kp"],[ikm,km,"km"]].each{ip,part,name->
            //def adj_phi = phi-(((sec-1)*60-(sec>4 ? 1 : 0))+(sec==4 ? 1 : 0)*(phi<0 ? 1 : 0))*360
            def (px,py,pz) = ['px','py','pz'].collect{partb.getFloat(it,ip)}
            def theta = Math.asin(Math.sqrt(px**2+py**2)/pz)*180/Math.PI
            def phi = Math.atan2(py,px)*180/Math.PI/1
            def adj_phi = phi+360*(phi<-30 ? 1 : 0)
            hists.computeIfAbsent("${gbname}_${name}_ThP",hThetaP).fill(theta, part.p())
            hists.computeIfAbsent("${gbname}_${name}_PhiP",hPhiP).fill(adj_phi, part.p())
            hists.computeIfAbsent("${gbname}_${name}_ThPhi",hThetaPhi).fill(theta, adj_phi)
          }
        }
    }
  }
}