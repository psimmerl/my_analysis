//run-groovy run.groovy /cache/clas12/rg-a/production/recon/fall2018/torus-1/pass1/v0/dst/train/skim4/skim4_005038.hipo
System.setProperty("java.awt.headless", "true")
import java.util.concurrent.TimeUnit
def mytime = System.currentTimeMillis()
import groovyx.gpars.GParsPool
import java.util.concurrent.ConcurrentHashMap
import java.util.concurrent.Executors
import java.util.concurrent.ScheduledExecutorService
import java.util.concurrent.atomic.AtomicInteger
import org.jlab.io.hipo.HipoDataSource
import org.jlab.clas.physics.LorentzVector
import org.jlab.groot.data.H1F
import org.jlab.groot.data.H2F
import clas12.mon.paul.EPKpKm_FD_mon
import org.jlab.jroot.ROOTFile
import java.io.File
import utils.KinTool
import my.Sugar
Sugar.enable()

fin = []
fout = ""
cut = ""
args.eachWithIndex{it,index->
  if (it.contains(".hipo") ) {fin.add(it)}
  if (it.contains(".root") ) {fout=it}
  if (it.contains(".json") ) {fjson=it; cut=args[index+1]}
}
println("fin: "+fin)
println("fout: "+fout)
println("fjson: "+fjson)
println("cut: "+cut)

def ecut = args.contains("ecut")
def pcut = args.contains("pcut")
def kpcut = args.contains("kpcut")
def kmcut = args.contains("kmcut")
def vzcut = args.contains("vzcut")
def cpcut = args.contains("cpcut")
def ckpcut = args.contains("ckpcut")
def ckmcut = args.contains("ckmcut")
def ikkcut = args.contains("ikkcut")
print(ecut);print(pcut);print(kpcut);print(kmcut);print(vzcut);print(cpcut);print(ckpcut);println(ckmcut);print(ikkcut)
def kaon_proc = new EPKpKm_FD_mon(fjson, cut, ecut, pcut, kpcut, kmcut, vzcut, cpcut, ckpcut, ckmcut, ikkcut)


def evcount = new AtomicInteger()
def evsum = new AtomicInteger()


def save = {
  ff = new ROOTFile(fout)
  kaon_proc.hists.each{h-> ff.addDataSet(h.value) }
  ff.close()
 
 evsum.set(evcount.get()+evsum.get())
  println "event count: "+evcount.get()
  println "  tol: "+evsum.get()
  evcount.set(0)
}
save()

def exe = Executors.newScheduledThreadPool(1)
exe.scheduleWithFixedDelay(save, 5, 30, TimeUnit.SECONDS)

GParsPool.withPool 5, {
  fin.eachParallel{fname->
    def reader = new HipoDataSource()
    reader.open(fname)
    while( reader.hasEvent() ) {
      evcount.getAndIncrement()
      def event = reader.getNextEvent()
      kaon_proc.processEvent(event)
    }
    reader.close()
  }
}

//if(kaon_proc.metaClass.respondsTo(kaon_proc, 'finish')) kaon_proc.finish()
exe.shutdown()
save()
mytime = Math.round((System.currentTimeMillis()-mytime)/1000/60)
println "Generated ${kaon_proc.hists.size()} Histograms in $mytime minutes"
