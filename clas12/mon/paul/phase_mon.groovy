package clas12.mon.paul

import org.jlab.clas.physics.LorentzVector
import org.jlab.groot.data.H1F
import org.jlab.groot.data.H2F
import java.util.concurrent.ConcurrentHashMap
import utils.KinTool

class phase_mon {
  def hists = new ConcurrentHashMap()

  def beam = LorentzVector.withPID(11,0,0,10.6)
  def target = LorentzVector.withPID(2212,0,0,0)

  def hThetaP = {new H2F("$it", "$it", 1000, 0, 90, 1000, 0, 10)}
  def hPhiP = {new H2F("$it", "$it", 1000, -180, 180, 1000, 0, 10)}
  def hThetaPhi = {new H2F("$it", "$it", 1000, 0, 90, 1000, -180, 180)}
  
  def banknames = ['REC::Particle','REC::Calorimeter']

  def buildHists() {
    for ( def sec = 1 ; sec < 7 ; sec++ ) {
      hists.computeIfAbsent("H2F_sec${sec}_ThetaP",hThetaP).fill(1000, 1000)
      //hists.computeIfAbsent("H2F_sec${sec}_PhiP",hPhiP).fill(1000, 1000)
    }
    hists.computeIfAbsent("H2F_PhiP",hPhiP).fill(1000, 1000)
    hists.computeIfAbsent("H2F_ThetaPhi",hThetaPhi).fill(1000, 1000)
  }
  
  def processEvent(event) {
    if(banknames.every{event.hasBank(it)}) {
      def (partb,calb) = banknames.collect{event.getBank(it)}

      (0..<partb.rows()).findAll{partb.getInt('pid',it)==11 && partb.getShort("status",it)<0}
        .each{iele->
          def ele = LorentzVector.withPID(11,*['px','py','pz'].collect{partb.getFloat(it,iele)})
          def sec = calb.getByte('sector',iele)
          
          def px = partb.getFloat('px',iele)
          def py = partb.getFloat('py',iele)
          def pz = partb.getFloat('pz',iele)
          def theta = Math.asin(Math.sqrt(px**2+py**2)/pz)*180/Math.PI
          def phi = Math.atan2(py,px)*180/Math.PI/1
          def adj_phi = phi//phi-(((sec-1)*60-(sec>4 ? 1 : 0))+(sec==4 ? 1 : 0)*(phi<0 ? 1 : 0))*360

          hists.computeIfAbsent("H2F_sec${sec}_ThetaP",hThetaP).fill(theta, ele.p())
          //hists.computeIfAbsent("H2F_sec${sec}_PhiP",hPhiP).fill(adj_phi, ele.p())
          hists.computeIfAbsent("H2F_PhiP",hPhiP).fill(adj_phi, ele.p())
          hists.computeIfAbsent("H2F_ThetaPhi",hThetaPhi).fill(theta, phi)
        }
    }
  }
}
