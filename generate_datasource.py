import requests
import json

import os
cwd = os.getcwd()
print("cwd =",cwd)

from string import Template

def GetSampleFromRouteros(cmd):
    url = "https://192.168.9.8/rest/" + cmd

    headers = {
      'Content-Type': 'application/json',
      'Access-Control-Request-Headers': '*',
    }

    try:
        response = requests.get( url,auth= ('admin', 'admin'),timeout=5, verify=False)
        
        response.raise_for_status()
        return response.json()
        
    except requests.exceptions.HTTPError as errh:
        print(errh)
    except requests.exceptions.ConnectionError as errc:
        print(errc)
    except requests.exceptions.Timeout as errt:
        print(errt)
    except requests.exceptions.RequestException as err:
        print(err)

    return None

# reconise the type of the structitem based on the value from sample
def GetTypedef(value):
    if value.isnumeric():
        foundtype = "TypeInt"
    elif value in ["false","true"]:
        foundtype = "TypeBool"
    else:
        foundtype = "TypeString"
    return foundtype

# return one structitem
# "address": {
#     Type:     schema.TypeString,
#     Computed: true,
# },
def GetGoTypedefStruct(key,value,nrtabs):
        structitemname = key.lower()    # only lowercase
        structitemname = structitemname.replace("-","_")    # no minus in name
        if structitemname == ".id":
            structitemname = "id"
        goschema  = '{tabs}"{name}": {{ // Sample = {key}: "{value}"\n'.format(tabs = nrtabs*'\t', name = structitemname, key=key, value=value)
        goschema += '{tabs}\tType:     schema.{stype},\n'.format(tabs = nrtabs*'\t', stype = GetTypedef(value))
        goschema += '{tabs}\tComputed: true,\n'.format(tabs = nrtabs*'\t')
        goschema += '{tabs}}},\n'.format(tabs = nrtabs*'\t')
        return goschema

def GenerateGODatasourceCode(cmd, sampleid,fp_provider_go):
    print("Working on/" + cmd)
    cmd_split = cmd.split('/')
    mapping = {"cmd" : cmd, "sampleid" : sampleid}
    
    response = GetSampleFromRouteros(cmd)

    if response:
        if response.__class__ == list:     # the sample return a list of objects, add 's' because of plural
            mapping["GoStructName"] = ''.join(i.capitalize() for i in cmd_split) + 's'
            mapping["gostructname"] = mapping["GoStructName"].lower()
            mapping["go_struct_name"] = "_".join(cmd_split) + 's'
            templatefile = "ListSample2DatasourceRouteros.tmpl"
            nrtabs = 6
            sample = response[0]    # the first item in the list is used to typedef the gostruct
        else:
            # singular, the sample conatins just one object with attributes
            mapping["GoStructName"] = ''.join(i.capitalize() for i in cmd_split)
            mapping["gostructname"] = mapping["GoStructName"].lower()
            mapping["go_struct_name"] = "_".join(cmd_split)
            templatefile = "Sample2DatasourceRouteros.tmpl"
            nrtabs = 5
            sample = response

        gofilename = "datasource_" + mapping["go_struct_name"]
        provider_go_line = '\t\t\t"routeros_' + mapping["go_struct_name"] + ':      Datasource' + mapping["GoStructName"] + '(),'
            
        fp = open(templatefile,"r")
        datasource_template = Template(fp.read())
        fp.close()

        mapping["schema"] = ""
        for item in sample.keys():
            mapping["schema"] += GetGoTypedefStruct(item, sample[item], nrtabs)
            
        fp = open("c:/tmp/" + gofilename + '.go',"w+")    
        fp.write(datasource_template.substitute(mapping))
        fp.close()

        fp = open("Test" + templatefile,"r")
        datasource_test_template = Template(fp.read())
        fp.close()
            
        fp = open("c:/tmp/" + gofilename + '_test.go',"w+")
        fp.write(datasource_test_template.substitute(mapping))
        fp.close()
        # add the following line to provider.go
        fp_provider_go.write(provider_go_line)

sampleddevice = GetSampleFromRouteros("system/resource")
sampleid = "{platform} {version} on {board-name} {cpu}-{architecture-name}".format(**sampleddevice)

fp_provider_go = open("lines_to_include_in_provider.go","w+")
GenerateGODatasourceCode("ip/arp",sampleid,fp_provider_go)
GenerateGODatasourceCode("certificate",sampleid,fp_provider_go)
fp_provider_go.close()
#GenerateGODatasourceCode("system/resource",sampleid)
