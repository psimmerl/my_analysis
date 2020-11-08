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

class EPKpKm_mon {
  def hists = new ConcurrentHashMap()

  def beam = LorentzVector.withPID(11,0,0,10.6)
  def target = LorentzVector.withPID(2212,0,0,0)

  def mm2_fit_data = new ConcurrentHashMap()

  def mm2 = true
  def phase = true
  def q2w = true
  def masspro = true
  def masskp = true
  def masskm = true

  def name = ""

  def hmm2 = {new H1F("$it","$it",250,-0.5,2)}
  
  def himpro = {new H1F("$it","$it",180,1.4,2.0)}
  def himk = {new H1F("$it","$it",180,0.95,1.5)}
  def him2D = {new H2F("$it","$it",250,0.5,5, 250, 0.8, 2.2)}
  def hvz = {new H1F("$it","$it",250,-20,20)}
  def hcoplane = {new H1F("$it","$it",250,0,10)}

  def hThetaP = {new H2F("$it", "$it", 1000, 0, 90, 1000, 0, 10)}
  def hPhiP = {new H2F("$it", "$it", 1000, -30, 330, 1000, 0, 10)}
  def hThetaPhi = {new H2F("$it", "$it", 1000, 0, 90, 1000, -30, 330)}

  def hW2D = {new H2F("$it", "$it", 1000, 0, 4.5, 1000, 0, 10)}
  
  def banknames = ['RUN::config', 'REC::Particle','REC::Calorimeter','REC::Cherenkov','REC::Traj']
  
  def EPKpKm_mon(name='',mm2=true,phase=true,q2w=true,masspro=false,masskp=false,masskm=false) {
    //setCuts(ele_cuts, pip_cuts, pim_cuts)
    setHists(mm2, phase, q2w, masspro, masskp, masskm)
    setName(name)
  }

  def setHists(mm2 = true, phase = true, q2w=true,masspro=true,masskp=true,masskm=true) {
    this.mm2 = mm2
    this.phase = phase
    this.q2w = q2w
    this.masspro = masspro
    this.masskp = masskp
    this.masskm = masskm
    if ( masspro || masskp || masskm ) {
      def slurper = new JsonSlurper()
      this.mm2_fit_data = new ConcurrentHashMap(slurper.parse(new File('/volatile/clas12/psimmerl/my_analysis/kaon/mm2_fits_no_mass_cut.json')))
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
          def mmE = beam+target-ele-pro-kp-km
          def improkp = pro+kp
          def improkm = pro+km
          def imkpkm  = kp+km
          
          def vzkp = partb.getFloat('vz', ikp) 
          def vzkm = partb.getFloat('vz', ikm)

          def prodet = (partb.getShort('status',ipro)/1000/1).toInteger()==2 ? 'FD':'CD'
          def kpdet = (partb.getShort('status',ikp)/1000/1).toInteger()==2 ? 'FD':'CD'
          def kmdet = (partb.getShort('status',ikm)/1000/1).toInteger()==2 ? 'FD':'CD'
          def detname = "pro_${prodet}_kp_${kpdet}_km_${kmdet}"
          def isgood = true

          if ( (masspro || masskp || masskm) && isgood ) {
            println(mm2_fit_data)
            def mu0pro  = mm2_fit_data["TOTAL_GOOD_mmpro_$detname"][1][1]
            def sig0pro = mm2_fit_data["TOTAL_GOOD_mmpro_$detname"][1][2]
            def mu0kp   = mm2_fit_data["TOTAL_GOOD_mm2kp_$detname"][1][1]
            def sig0kp  = mm2_fit_data["TOTAL_GOOD_mm2kp_$detname"][1][2]
            def mu0km   = mm2_fit_data["TOTAL_GOOD_mm2km_$detname"][1][1]
            def sig0km  = mm2_fit_data["TOTAL_GOOD_mm2km_$detname"][1][2]
            def mu0me   = mm2_fit_data["TOTAL_GOOD_mmE"][1][1]
            def sig0me  = mm2_fit_data["TOTAL_GOOD_mmE"][1][2]
            if (masspro == true && isgood) { isgood = Math.abs((mm2pro.mass()-mu0pro)/sig0pro/1)<4 }
            if (masskp == true && isgood)  { isgood = Math.abs((mm2kp.mass2()-mu0kp)/sig0kp/1)<4 }
            if (masskm == true && isgood)  { isgood = Math.abs((mm2km.mass2()-mu0km)/sig0km/1)<4 }
            if ( isgood ) { isgood = Math.abs((mmE.e()-mu0me)/sig0me/1)<4 }
            if ( isgood ) { isgood = (vzkp-vzkm) <= 5 }
            if ( isgood ) { isgood = mm2pro.vect().theta(pro.vect()) <= 9 }
            if ( isgood ) { isgood = mm2kp.vect().theta(kp.vect()) <= 9 }
            if ( isgood ) { isgood = mm2km.vect().theta(km.vect()) <= 9 }


          }

          def gbname = name+(isgood ? '_GOOD':'_BAD')

					if ( mm2 ) {
            hists.computeIfAbsent("${gbname}_mm2kp_$detname",hmm2).fill(mm2kp.mass2())
            hists.computeIfAbsent("${gbname}_mm2km_$detname",hmm2).fill(mm2km.mass2())
            hists.computeIfAbsent("${gbname}_mmpro_$detname",hmm2).fill(mm2pro.mass())
          }
          def (px,py,pz) = ['px','py','pz'].collect{partb.getFloat(it,iele)}
          def theta = Math.asin(Math.sqrt(px**2+py**2)/pz)*180/Math.PI
          def phi = Math.atan2(py,px)*180/Math.PI/1
          //def adj_phi = phi-(((sec-1)*60-(sec>4 ? 1 : 0))+(sec==4 ? 1 : 0)*(phi<0 ? 1 : 0))*360
          def adj_phi = phi+360*(phi<-30 ? 1 : 0)
          if ( phase ) {
            hists.computeIfAbsent("${gbname}_H2F_sec${sec}_ThetaP",hThetaP).fill(theta, ele.p())
            hists.computeIfAbsent("${gbname}_H2F_PhiP",hPhiP).fill(adj_phi, ele.p())
            hists.computeIfAbsent("${gbname}_H2F_ThetaPhi",hThetaPhi).fill(theta, adj_phi)
          }
          if ( true ) {//brandon )
            hists.computeIfAbsent("${gbname}_mmE",hmm2).fill(mmE.e())
           
            hists.computeIfAbsent("${gbname}_improkp",himpro).fill(improkp.mass())
            hists.computeIfAbsent("${gbname}_improkm",himpro).fill(improkm.mass())
            hists.computeIfAbsent("${gbname}_imkpkm",himk).fill(imkpkm.mass())
            hists.computeIfAbsent("${gbname}_imkpkm_pkm",him2D).fill(improkm.mass(), imkpkm.mass())
           
            hists.computeIfAbsent("${gbname}_vzkpvzkm",hvz).fill(vzkp-vzkm)
           
            hists.computeIfAbsent("${gbname}_coplanep",hcoplane).fill(mm2pro.vect().theta(pro.vect()))
            hists.computeIfAbsent("${gbname}_coplanekp",hcoplane).fill(mm2kp.vect().theta(kp.vect()))
            hists.computeIfAbsent("${gbname}_coplanekm",hcoplane).fill(mm2km.vect().theta(km.vect()))
                                   
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
