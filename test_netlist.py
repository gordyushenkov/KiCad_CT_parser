from __future__ import print_function

import kicad_netlist_reader
from netlist_components import KicadNetlist, KicadNet, KicadNode

import csv
import sys

fn = "C:\\Gordiushenkov\\cabling\\Products\\SH.056.51 Fast charger\\SH.056.51 Fast charger.kicad_sch"
fn = "C:\\Gordiushenkov\\cabling\\Products\\SH.056.51 Fast charger\\SH.056.51 Fast charger.xml"

NL = KicadNetlist.from_xml_file(fn)

print(NL)
NL_filt = NL.filter_netlist(2)
print(NL_filt)
CT = NL.filter_netlist(2).get_CT()
import pprint
pprint.pprint(CT)