#!/usr/bin/env python 

import multiprocessing,os,netifaces

DEBUG=True

"""
root@opti330:/proc/net/pktgen# ls
kpktgend_0  kpktgend_1  pgctrl
"""
####

def get_local_mac(interface):
  """Return the physical address for a given NIC"""
  pass

def get_remote_mac(address):
  """Return mac of remote host given an IP"""
  f = open ("/proc/net/arp","r")
  for l in f:
    entry = l.rstrip().split()
    if address == entry[0]:
      return entry[3]
  # TODO handle gateway

def pgset(command,thread=0):
    f = open ("/proc/net/pktgen/kpktgend_"+str(thread),"a")
    f.write(command)

def pgset_iface(command,interface="eth0"):
    f = open ("/proc/net/pktgen/"+interface,"a")
    f.write(command)

class PacketGenerator(object):
  def __init__(self,interface="eth0",debug=True):
    os.system("modprobe pktgen")
    self.debug = debug
    self.cpus = multiprocessing.cpu_count()
    self.interface = interface
    self.threads = 1

    if self.debug:
      print "Removing interface from threads"
    for c in range(self.cpus):
      pgset("rem_device_all",c)
      pgset("add_device "+self.interface,c)

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

  def configure(self,target,delay=100000,size=250,count=10,thread=0):
    commands = []
    commands.append("dst " + target)
    commands.append("count " + str(count))
    commands.append("delay " + str(delay))
    commands.append("pkt_size " + str(size))

    if target == "127.0.0.1":
      commands.append("dst_mac 00:00:00:00:00:00")
      commands.append("src_mac 00:00:00:00:00:00")
    else:
      os.system("ping -c 5 "+ target)
      commands.append("dst_mac "+ get_remote_mac(target))

    for c in commands:
      if self.debug:
        print c
      pgset_iface(c,self.interface)

  def start(self):
    pass

  def stop(self):
    pass

  def destroy(self):
    os.system("rmmod pktgen")

if __name__ == "__main__":
  pg = PacketGenerator()
  pg.thread_status()
  pg.configure("192.168.2.203")
  pg.eth_status()
