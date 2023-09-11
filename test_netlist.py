from __future__ import print_function

import kicad_netlist_reader
import csv
import sys

fn = "C:\\Gordiushenkov\\cabling\\Products\\SH.056.51 Fast charger\\SH.056.51 Fast charger.kicad_sch"
fn = "C:\\Gordiushenkov\\cabling\\Products\\SH.056.51 Fast charger\\SH.056.51 Fast charger.xml"

net = kicad_netlist_reader.netlist(fn)
print(net)
for n in net.getNets():
    print()
    print(n)
    print(n.name)
    print(n.attributes)
    for ch in n.children:
        print(ch.name)
        print(ch.attributes)

print(net.getInterestingComponents())