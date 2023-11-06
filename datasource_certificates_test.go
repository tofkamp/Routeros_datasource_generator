package routeros

// Script generated with sample from device MikroTik 7.11.2 (stable) on CHR AMD-x86_64

import (
        "testing"

        "github.com/hashicorp/terraform-plugin-testing/helper/resource"
)

const testDatasourceCertificates = "data.routeros_certificates.data"

func TestAccDatasourceCertificatesTest_basic(t *testing.T) {
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
                                                Config: testAccDatasourceCertificatesConfig(),
                                                Check: resource.ComposeTestCheckFunc(
                                                        testResourcePrimaryInstanceId(testDatasourceIpRoutes),
                                                ),
                                        },
                                },
                        })

                })
        }
}

func testAccDatasourceCertificatesConfig() string {
        return providerConfig + `

data "routeros_certificates" "data" {}
`
}
