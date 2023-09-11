import csv
from netlist_components import KicadNetlist

fn = "C:\\Gordiushenkov\\cabling\\Products\\SH.056.51 Fast charger\\SH.056.51 Fast charger.xml"

NL = KicadNetlist.from_xml_file(fn)
CT = NL.filter_netlist(2).get_CT()

file_path = 'test.csv'

# Open the CSV file in write mode
with open(file_path, mode='w', newline='') as csv_file:
    # Create a CSV writer object
    csv_writer = csv.writer(csv_file)

    # Write the data to the CSV file
    for ref_nets in CT.values():
        for net, nodes in ref_nets.items():
            csv_writer.writerow([net.name] + [f'{node.ref}-{node.pin}' for node in nodes])
