package routeros

// Script generated from sampled device MikroTik 7.11.2 (stable) on CHR AMD-x86_64

import (
        "testing"

        "github.com/hashicorp/terraform-plugin-testing/helper/resource"
)

const testDatasourceIpArpss = "data.routeros_ip_arpss.routes"

func TestAccDatasourceIpArpssTest_basic(t *testing.T) {
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
                                                Config: testAccDatasourceIpArpssConfig(),
                                                Check: resource.ComposeTestCheckFunc(
                                                        testResourcePrimaryInstanceId(testDatasourceIpRoutes),
                                                ),
                                        },
                                },
                        })

                })
        }
}

func testAccDatasourceIpArpssConfig() string {
        return providerConfig + `

data "routeros_ip_arpss" "routes" {}
`
}
