package clas12.mon.paul

import org.jlab.clas.physics.LorentzVector
import org.jlab.groot.data.H1F
import org.jlab.groot.data.H2F
import java.util.concurrent.ConcurrentHashMap
import utils.KinTool

class q2w_mon {
  def hists = new ConcurrentHashMap()

  def beam = LorentzVector.withPID(11,0,0,10.6)
  def target = LorentzVector.withPID(2212,0,0,0)

  //def hW = {new H1F("$it","$it",1000,0,4.5)}
  def hW2D = {new H2F("$it", "$it", 1000, 0, 4.5, 1000, 0, 10)}

  def banknames = ['REC::Particle','REC::Calorimeter']
  
  def buildHists() {
    for ( def sec = 1 ; sec < 7 ; sec++ ) { 
      /*for ( def Q2 = 0 ; Q2 < 10 ; Q2++ ) {
        hists.computeIfAbsent("hq2w_sec${sec}_q2bin${(int)Math.floor(Q2)}",hW)
      }*/
      hists.computeIfAbsent("H2F_sec${sec}_q2w",hW2D).fill(1000,1000)
    }
  }

  def processEvent(event) {
    if(banknames.every{event.hasBank(it)}) {
      def (partb,calb) = banknames.collect{event.getBank(it)}

      (0..<partb.rows()).findAll{partb.getInt('pid',it)==11 && partb.getShort("status",it)<0}
        .each{iele->
          def ele = LorentzVector.withPID(11,*['px','py','pz'].collect{partb.getFloat(it,iele)})
          def Q2 = KinTool.calcQ2(beam, ele)
          def sec = calb.getByte('sector',iele)       
          def eX  = beam+target-ele

          if (Q2<10){
            //hists.computeIfAbsent("hq2w_sec${sec}_q2bin${(int)Math.floor(Q2)}",hW).fill(eX.mass())
            hists.computeIfAbsent("H2F_sec${sec}_q2w",hW2D).fill(eX.mass(), Q2)
          }
        }
    }
  }
}
