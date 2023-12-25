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

# class KicadComponent(NamedTuple):
#     ref: str = ''
#     priority: int = 0
#
#     def __repr__(self):
#         if self.priority:
#             return f'[{self.priority}]{self.ref}'
#         else:
#             return f'{self.ref}'

class KicadNetlist():
    NETNAME_WIDTH = 15
    def __init__(self):
        self._netlist = {}
        self._complist = {} # ref: {attr: value}

    def add_net(self, net:KicadNet, nodes:list):
        self._netlist[net] = nodes

    def __repr__(self):
        txt = ''
        for net, nodes in self._netlist.items():
            txt += f'{net.name:<{self.NETNAME_WIDTH}}'
            for n in nodes:
                if n.pin:
                    txt += f' {n.ref}-{n.pin}'
                else:
                    txt += f' {n.ref}'
            txt += '\n'
        for ref, attrib in self._complist.items():
            txt += f'{ref}: {attrib}\n'
        return txt

    def filter_netlist(self, min_node_N=0):
        new_NL = KicadNetlist()
        new_NL._netlist = {net:node for net, node in self._netlist.items() if len(node) >= min_node_N}
        refs = new_NL.get_ref_list()
        new_NL._complist = {comp:attribs for comp, attribs in self._complist.items() if comp in refs}
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
            for i, n in enumerate(nodes):
                if ref == n.ref:
                    poped_dict[net] = [n] + self._netlist[net][:i] + self._netlist[net][i+1:]
                    used_nets.append(net)
                    break
        for n in used_nets:
            del self._netlist[n]
        return poped_dict


    def get_CT(self):
        ref_set = self.get_ref_list()
        refs_with_priority = [r for r in ref_set if self._complist[r].get('priority', 0)]
        refs_without_priority = [r for r in ref_set if not self._complist[r].get('priority', 0)]
        refs_with_priority = sorted(refs_with_priority, key=lambda x: self._complist[x]['priority'])
        refs_without_priority = sorted(refs_without_priority, key=custom_sort_key)
        report = {}
        for ref in refs_with_priority:
            ref_dict = self.pop_nets_by_node_ref(ref)
            report[ref] = ref_dict
        for ref in refs_without_priority:
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

        ref_list = NL.get_ref_list()
        for ref in ref_list:
            NL._complist[ref] = {'priority':0}

        for comp in netlist.components:
            ref = comp.getRef()
            if ref in ref_list:
                priority = comp.getField('priority')
                if priority:
                    NL._complist[ref]['priority'] = priority

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
    # print(filtered)
    filtered.get_CT()
    refs = NL.get_ref_list()
    print(refs)