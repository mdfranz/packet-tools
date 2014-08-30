#!/usr/bin/env python 

import multiprocessing,os

DEBUG=True

"""
root@opti330:/proc/net/pktgen# ls
kpktgend_0  kpktgend_1  pgctrl
"""
####

class PacketGenerator(object):
  def __init__(self,interface="eth0"):
    self.cpus = multiprocessing.cpu_count()
    self.interface = interface
    for c in range(self.cpus):
      f = open ("/proc/net/pktgen/kpktgend_"+str(c),"a")
      f.write("rem_device_all")

  def eth_status(self):
    f = open ("/proc/net/pktgen/"+self.interface,"r") 
    print "\n[%s]" % f.name
    for l in f:
      print l.rstrip()

  def thread_status(self):
    for c in range(self.cpus):
      f = open ("/proc/net/pktgen/kpktgend_"+str(c),"r") 
      print "\n[%s]" % f.name
      for l in f:
        print l.rstrip()

class PacketSurge(object):
  def __init__(self,target,pps_rate,size=250,count=100):
    pass

if __name__ == "__main__":
  pg = PacketGenerator()
  pg.thread_status()
