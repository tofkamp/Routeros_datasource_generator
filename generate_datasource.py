import requests
import json

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

def GenerateGODatasourceCode(cmd, sample_id):

    cmd_split = cmd.split('/')
    GoStructName = ''.join(i.capitalize() for i in cmd_split)
    gostructname = GoStructName.lower()

    response = GetSampleFromRouteros(cmd)

    if response:
        
        if response.__class__ == list:
            gofilename = "datasource_" + cmd.replace('/','_') + "s.go"
            templatefile = "ListSample2DatasourceRouteros.tmpl"
            provider_go_line = '\t\t\t"routeros_' + cmd.replace('/','_') + 's":      Datasource' + GoStructName + 's(),'
            nrtabs = 6
            sample = response[0]    # the first item is used to typedef
    #        print("ini_list1 is a list")
        else:
            gofilename = "datasource_" + cmd.replace('/','_') + ".go"
            templatefile = "Sample2DatasourceRouteros.tmpl"
            provider_go_line = '\t\t\t"routeros_' + cmd.replace('/','_') + '":      Datasource' + GoStructName + '(),'
            nrtabs = 5
            sample = response
    #        print("ini_list1 is not a list")

        fp = open("c:/tmp/" + templatefile,"r")
        datasource_template = Template(fp.read())
        fp.close()

        schema = ""
        for item in sample.keys():
            schema += GetGoTypedefStruct(item, sample[item], nrtabs)
            
        fp = open("c:/tmp/" + gofilename,"w+")
        fp.write(datasource_template.substitute(schema = schema,cmd = cmd, gostructname = gostructname,Gostructname = GoStructName, sampleid = sample_id))
        fp.close()

        print("Add this line in provider.go:",provider_go_line)

sampleddevice = GetSampleFromRouteros("system/resource")
sample_id = "{platform} {version} on {board-name} {cpu}-{architecture-name}".format(**sampleddevice)

GenerateGODatasourceCode("ip/arp",sample_id)
GenerateGODatasourceCode("system/resource",sample_id)
GenerateGODatasourceCode("certificate",sample_id)
