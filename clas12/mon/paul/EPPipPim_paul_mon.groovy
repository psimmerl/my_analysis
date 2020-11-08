package clas12.mon.paul

import org.jlab.clas.physics.LorentzVector
import org.jlab.groot.data.H1F
import org.jlab.groot.data.H2F
import java.util.concurrent.ConcurrentHashMap
import utils.KinTool


class EPPipPim_paul_mon {
  def hists = new ConcurrentHashMap()

  def beam = LorentzVector.withPID(11,0,0,10.6)
  def target = LorentzVector.withPID(2212,0,0,0)

  def hmm2 = {new H1F("$it","$it",250,-0.5,2)}
  def him = {new H1F("$it","$it",180,0.2,2)}

  def hThetaP = {new H2F("$it", "$it", 1000, 0, 90, 1000, 0, 10)}
  def hPhiP = {new H2F("$it", "$it", 1000, -180, 180, 1000, 0, 10)}
  def hThetaPhi = {new H2F("$it", "$it", 1000, 0, 90, 1000, -180, 180)}

  def hW2D = {new H2F("$it", "$it", 1000, 0, 4.5, 1000, 0, 10)}
  
  def banknames = ['REC::Particle', 'REC::Calorimeter']
  def buildHists() {
    /*hists.computeIfAbsent("mm2pip_FD",hmm2).fill(100)
    hists.computeIfAbsent("mm2pim_FD",hmm2).fill(100)
    //hists.computeIfAbsent("mm2pro_FD",hmm2).fill(100)
    hists.computeIfAbsent("mmpro_FD",hmm2).fill(100)
    hists.computeIfAbsent("mm2pip_CD",hmm2).fill(100)
    hists.computeIfAbsent("mm2pim_CD",hmm2).fill(100)
    //hists.computeIfAbsent("mm2pro_CD",hmm2).fill(100)
    hists.computeIfAbsent("mmpro_CD",hmm2).fill(100)
    */
  }
  
  def processEvent(event) {
    if(banknames.every{event.hasBank(it)}) {
      def (partb,calb) = banknames.collect{event.getBank(it)}

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
          def mm2pip = beam+target-ele-pro-pim
          def mm2pim = beam+target-ele-pro-pip
          def mm2pro = beam+target-ele-pip-pim

          def prodet = (partb.getShort('status',ipro)/1000).toInteger()==2 ? 'FD':'CD'
          def pipdet = (partb.getShort('status',ipip)/1000).toInteger()==2 ? 'FD':'CD'
          def pimdet = (partb.getShort('status',ipim)/1000/1).toInteger()==2 ? 'FD':'CD'

          hists.computeIfAbsent("mm2pip_$pimdet",hmm2).fill(mm2pip.mass2())
          hists.computeIfAbsent("mm2pim_$pipdet",hmm2).fill(mm2pim.mass2())
          hists.computeIfAbsent("mm2pro_$prodet",hmm2).fill(mm2pro.mass2())
          hists.computeIfAbsent("mmpro_$prodet",hmm2).fill(mm2pro.mass())

          def sec = calb.getByte('sector',iele)
          def (px,py,pz) = ['px','py','pz'].collect{partb.getFloat(it,iele)}
          def theta = Math.asin(Math.sqrt(px**2+py**2)/pz)*180/Math.PI
          def phi = Math.atan2(py,px)*180/Math.PI/1
          def adj_phi = phi//phi-(((sec-1)*60-(sec>4 ? 1 : 0))+(sec==4 ? 1 : 0)*(phi<0 ? 1 : 0))*360
          
          hists.computeIfAbsent("H2F_sec${sec}_ThetaP",hThetaP).fill(theta, ele.p())
          hists.computeIfAbsent("H2F_sec${sec}_PhiP",hPhiP).fill(adj_phi, ele.p())
          hists.computeIfAbsent("H2F_ThetaPhi",hThetaPhi).fill(theta, phi)
        
          def Q2 = KinTool.calcQ2(beam, ele)
          def eX  = beam+target-ele
            
          hists.computeIfAbsent("H2F_sec${sec}_q2w",hW2D).fill(eX.mass(), Q2)
        }
    }
  }
}
