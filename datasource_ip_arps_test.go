package routeros

// Script generated with sample from device MikroTik 7.11.2 (stable) on CHR AMD-x86_64

import (
        "testing"

        "github.com/hashicorp/terraform-plugin-testing/helper/resource"
)

const testDatasourceIpArps = "data.routeros_ip_arps.data"

func TestAccDatasourceIpArpsTest_basic(t *testing.T) {
        for _, name := range testNames {
                t.Run(name, func(t *testing.T) {
                        resource.Test(t, resource.TestCase{
                                PreCheck: func() {
                                        testAccPreCheck(t)
                                        testSetTransportEnv(t, name)
                                },
                                ProviderFactories: testAccProviderFactories,
                                Steps: []resource.TestStep{
                                        {
                                                Config: testAccDatasourceIpArpsConfig(),
                                                Check: resource.ComposeTestCheckFunc(
                                                        testResourcePrimaryInstanceId(testDatasourceIpRoutes),
                                                ),
                                        },
                                },
                        })

                })
        }
}

func testAccDatasourceIpArpsConfig() string {
        return providerConfig + `

data "routeros_ip_arps" "data" {}
`
}
