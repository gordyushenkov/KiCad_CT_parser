import tkinter as tk
from tkinter import filedialog
import traceback
import csv
from netlist_components import KicadNetlist
import os

DEBUG_OUTPUT = False

filename_xml=""#"C:\\Gordiushenkov\\Manufacturing\\Outsourcing\\EV48.01_11339_M.zip"
def open_xml():
    global filename_xml
    filename_xml = filedialog.askopenfilename(filetypes=[("xml files", "*.xml"), ("All files", "*.*")])
    label_xml_file.config(text=filename_xml)

def generate():
    try:
        NL = KicadNetlist.from_xml_file(filename_xml)
        CT = NL.filter_netlist(2).get_CT()

        file_name_without_path = os.path.basename(filename_xml)
        file_name, file_extension = os.path.splitext(file_name_without_path)
        dir_path = os.path.dirname(os.path.abspath(filename_xml))
        output_fn = os.path.join(dir_path, (file_name + ' CT.csv'))
        with open(output_fn, mode='w', newline='') as csv_file:
            # Create a CSV writer object
            csv_writer = csv.writer(csv_file)
            headers = ['N', 'Netname', 'From', 'To']
            csv_writer.writerow(headers)
            # Write the data to the CSV file
            row_n = 1
            for ref_nets in CT.values():
                for net, nodes in ref_nets.items():
                    row = [f'{row_n}', net.name]
                    for node in nodes:
                        if node.pin:
                            row.append(f'{node.ref}-{node.pin}')
                        else:
                            row.append(f'{node.ref}')
                    csv_writer.writerow(row)
                    row_n += 1
        msg = 'CT sucessfully generated:\n'
        msg += f'{output_fn}'
        text_box_output.delete('1.0', tk.END)
        text_box_output.insert('1.0', msg)

    except Exception as e:
        msg = 'Runtime error occured:\n'

        traceback_info = traceback.format_exc()
        msg += f'{traceback_info}'
        text_box_output.delete('1.0', tk.END)
        text_box_output.insert('1.0', msg)

app = tk.Tk()
app.title("CT creator")

frame_arch = tk.Frame(app)
frame_arch.pack(fill="x")
frame_erp = tk.Frame(app)
frame_erp.pack(fill="x")
frame_output = tk.Frame(app)
frame_output.pack()

PADX = 5
PADY = 5
TEXTWIDTH = 100

open_button = tk.Button(frame_arch, text="XML file", command=open_xml)
open_button.pack(padx=PADX, pady=PADY, side='left')
label_xml_file = tk.Label(frame_arch, text="Choose kicad xml file")
label_xml_file.pack(pady=PADY, side='left')


compare_button = tk.Button(frame_output, text="Generate", command=generate)
compare_button.pack(pady=PADY,)

text_box_output = tk.Text(frame_output, wrap=tk.WORD, height=10, width=TEXTWIDTH)
text_box_output.pack(fill=tk.BOTH, expand=True)

Instruction = """How to use:
1. Open schematics in Kicad
2. Choose menu Tool->Generate BOM...
3. Run any BOM generator by pressing "Generate" button
4. Chose the xml file created in the design directory by pressing the button above
5. Press generate button"""
text_box_output.insert('1.0', Instruction)

if DEBUG_OUTPUT:
    text_box_dbg = tk.Text(frame_output, wrap=tk.WORD, height=10, width=TEXTWIDTH)
    text_box_dbg.pack(fill=tk.BOTH, expand=True)
app.mainloop()