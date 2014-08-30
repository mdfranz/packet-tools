#!/usr/bin/env python 

import multiprocessing,os

DEBUG=True

"""
root@opti330:/proc/net/pktgen# ls
kpktgend_0  kpktgend_1  pgctrl
"""
####

def pg_set(command,thread=0):
    f = open ("/proc/net/pktgen/kpktgend_"+str(thread),"a")
    f.write(command)

class PacketGenerator(object):
  def __init__(self,interface="eth0"):
    os.system("modprobe pktgen")
    self.cpus = multiprocessing.cpu_count()
    self.interface = interface
    for c in range(self.cpus):
      pg_set("rem_device_all",c)
      pg_set("add_device "+self.interface,c)

  def eth_status(self):
    f = open ("/proc/net/pktgen/"+self.interface,"r") 
    print "\n[%s]" % f.name
    for l in f:
      print l.rstrip()

  def thread_status(self):
    #for c in range(self.cpus):
    for c in range(1):
      f = open ("/proc/net/pktgen/kpktgend_"+str(c),"r") 
      print "\n[%s]" % f.name
      for l in f:
        print l.rstrip()

  def configure(self,target,pps_rate,size=250,count=100,thread=0):
    commands = []
    commands.append("dst " + target)
    commands.append("count " + str(count))
    commands.append("pkt_size " + str(size))

  def destroy(self):
    os.system("rmmod pktgen")

if __name__ == "__main__":
  pg = PacketGenerator()
  pg.thread_status()
  pg.eth_status()
  pg.destroy()
