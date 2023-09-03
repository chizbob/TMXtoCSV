import sys
import os
from lxml import etree
import pandas as pd
import ast

input_file = os.path.basename(sys.argv[1:][0])

xml_tree = etree.parse(input_file)

trans_units = xml_tree.findall(".//tu")

d = []
for trans_unit in trans_units:
    row = dict(trans_unit.attrib)
    props = trans_unit.findall(".//prop")
    for p in props:
        if p.attrib['type'] == 'x-project-reference-id' :
            refid_dict = ast.literal_eval(p.text)
            row[p.attrib['type']] = refid_dict['ids'][0]
        else :
            row[p.attrib['type']] = p.text
    tuvs = trans_unit.findall(".//tuv")
    for tuv in tuvs :
        lang_code = tuv.attrib.values()[0]
        seg = tuv.findall(".//seg")[0]
        #print(lang_code)
        #print(seg.text)
        row[lang_code] = seg.text
    print(row)
    d.append(row)

df = pd.DataFrame.from_dict(d)

df.to_csv("TMX_" + os.path.splitext(input_file)[0] + ".csv",index=False)
