# Routeros_datasource_generator
Sample an mikrotik switch with REST request, and then generate datasource go-code for terraform/OpenToFu provider Routeros https://registry.terraform.io/providers/terraform-routeros/routeros/latest
Also some testcode is generated.

# Examples of output
The datasource_* files are examples of output of the program

# Problems/issue
The code generator template of just one object is not working yet. For example the output of the /system/resource is just one object.
The test code is not tested yet
