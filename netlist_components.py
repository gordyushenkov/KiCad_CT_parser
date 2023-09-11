from typing import NamedTuple
import kicad_netlist_reader
import re

class KicadNet(NamedTuple):
    name: str = ''
    code: str = ''

    def __repr__(self):
        return f'net {self.name} code:{self.code}'

    @staticmethod
    def from_xml_elem(node):
        name = node.attributes['name']
        if name.startswith('/'):
            name = name[1:]
        return KicadNet(name=name, code=node.attributes['code'])


class KicadNode(NamedTuple):
    ref: str = ''
    pin: str = ''

    def __repr__(self):
        return f'{self.ref} pin:{self.pin}'

    @staticmethod
    def from_xml_elem(node):
        return KicadNode(ref=node.attributes['ref'], pin=node.attributes['pin'])

class KicadNetlist():
    NETNAME_WIDTH = 15
    def __init__(self):
        self._netlist = {}

    def add_net(self, net:KicadNet, nodes:list):
        self._netlist[net] = nodes

    def __repr__(self):
        txt = ''
        for net, nodes in self._netlist.items():
            txt += f'{net.name:<{self.NETNAME_WIDTH}}'
            for n in nodes:
                txt += f' {n.ref}-{n.pin}'
            txt += '\n'
        return txt

    def filter_netlist(self, min_node_N=0):
        new_NL = KicadNetlist()
        new_NL._netlist = {net:node for net, node in self._netlist.items() if len(node) >= min_node_N}
        return new_NL

    def get_ref_list(self):
        unique_values = set()

        # Iterate through the dictionaries and collect unique values from the 'scores' key
        for nodes in self._netlist.values():
            unique_values.update({n.ref for n in nodes})
        return unique_values

    def pop_nets_by_node_ref(self, ref):
        poped_dict = {}
        used_nets = []
        for net, nodes in self._netlist.items():
            if ref in [n.ref for n in nodes]:
                poped_dict[net] = self._netlist[net]
                used_nets.append(net)
        for n in used_nets:
            del self._netlist[n]
        return poped_dict


    def get_CT(self):
        refs = sorted(self.get_ref_list(), key=custom_sort_key)
        report = {}
        netlist = self._netlist
        for ref in refs:
            ref_dict = self.pop_nets_by_node_ref(ref)
            report[ref] = ref_dict
        return report
    @staticmethod
    def from_xml_file(fn):
        netlist = kicad_netlist_reader.netlist(fn)
        NL = KicadNetlist()
        for n in netlist.getNets():
            net = KicadNet.from_xml_elem(n)
            nodes = [KicadNode.from_xml_elem(e) for e in n.getChildren(name="node")]
            NL.add_net(net, nodes)
        return NL

def custom_sort_key(value):
    # Use regular expression to split the value into non-digits and digits parts
    parts = re.split(r'(\d+)', value)
    # Convert the digits part to an integer for sorting
    return (parts[0], int(parts[1]))

def test_getting_comp_list(netlist):
    comps = netlist.getInterestingComponents()
    for c in comps:
        print(f'{c.getRef()} {c.getPartName()}')

if __name__ == '__main__':
    fn = "C:\\Gordiushenkov\\cabling\\Products\\SH.056.51 Fast charger\\SH.056.51 Fast charger.xml"

    NL = KicadNetlist.from_xml_file(fn)

    # print(NL)
    filtered = NL.filter_netlist(2)
    filtered.get_CT()