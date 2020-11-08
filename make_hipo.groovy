///cache/clas12/rg-a/production/recon/fall2018/torus-1/pass1/v0/dst/train/skim4/skim4_005038.hipo
System.setProperty("java.awt.headless", "true")
import groovyx.gpars.GParsPool
import java.util.concurrent.CopyOnWriteArrayList
import java.util.concurrent.Executors
import java.util.concurrent.ScheduledExecutorService
import java.util.concurrent.TimeUnit
import java.util.concurrent.atomic.AtomicInteger
import org.jlab.io.hipo.HipoDataSource
import org.jlab.io.hipo.HipoDataSync
import org.jlab.clas.physics.LorentzVector
def mytime = System.currentTimeMillis()

def evcount = new AtomicInteger()
def evsum = new AtomicInteger()
def evtol = new AtomicInteger()
def events = new CopyOnWriteArrayList()

def r1 = new HipoDataSource()
r1.open(args[0])
def writer = r1.createWriter()//new HipoDataSync()
r1.close()
writer.open("/volatile/clas12/psimmerl/my_analysis/kaon/kaon_FD_events.hipo")
def save = {
  def wevents = events.clone()
  wevents.each{writer.writeEvent(it)}
  events.removeAll(wevents)
 
  evsum.set(evcount.get()+evsum.get())
  println "event count: "+evcount.get()
  println "  tol: "+evsum.get()
  evcount.set(0)
}
save()

def exe = Executors.newScheduledThreadPool(1)
exe.scheduleWithFixedDelay(save, 5, 30, TimeUnit.SECONDS)

def banknames = ['RUN::config', 'REC::Particle','REC::Calorimeter','REC::Cherenkov','REC::Traj']
GParsPool.withPool 5, {
  args.eachParallel{fname->
    def reader = new HipoDataSource()
    reader.open(fname)
    while( reader.hasEvent() ) {
      evtol.getAndIncrement()
      def event = reader.getNextEvent()
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
            def pd = (partb.getShort('status',ipro)/1000/1).toInteger()==2
            def kpd = (partb.getShort('status',ikp)/1000/1).toInteger()==2
            def kmd = (partb.getShort('status',ikm)/1000/1).toInteger()==2
            if (pd && kpd && kmd) {
              //print(pd);print(kpd);println(kmd);
              evcount.getAndIncrement()
              events.add(event)
            }
          }
      }
    }
    reader.close()
  }
}

exe.shutdown()
save()
writer.close()
mytime = Math.round((System.currentTimeMillis()-mytime)/1000/60)
println "Collected ${evsum.get()} events (${evsum.get()/evtol.get()*100}%) in $mytime minutes"
