package routeros

// Script generated from sampled device MikroTik 7.11.2 (stable) on CHR AMD-x86_64

import (
	"context"

	"github.com/hashicorp/terraform-plugin-sdk/v2/diag"
	"github.com/hashicorp/terraform-plugin-sdk/v2/helper/schema"
)

func DatasourceCertificates() *schema.Resource {
	return &schema.Resource{
		ReadContext: datasourceCertificatesRead,
		Schema: map[string]*schema.Schema{
			MetaResourcePath: PropResourcePath("/certificate"),
			MetaId:           PropId(Id),

			KeyFilter: PropFilterRw,
			"Certificates": {
				Type:     schema.TypeList,
				Computed: true,
				Elem: &schema.Resource{
					Schema: map[string]*schema.Schema{
						"id": { // Sample = .id: "*1"
							Type:     schema.TypeString,
							Computed: true,
						},
						"akid": { // Sample = akid: ""
							Type:     schema.TypeString,
							Computed: true,
						},
						"common_name": { // Sample = common-name: "home.arpa"
							Type:     schema.TypeString,
							Computed: true,
						},
						"country": { // Sample = country: "AU"
							Type:     schema.TypeString,
							Computed: true,
						},
						"crl": { // Sample = crl: "false"
							Type:     schema.TypeBool,
							Computed: true,
						},
						"days_valid": { // Sample = days-valid: "45"
							Type:     schema.TypeInt,
							Computed: true,
						},
						"digest_algorithm": { // Sample = digest-algorithm: "sha512"
							Type:     schema.TypeString,
							Computed: true,
						},
						"expires_after": { // Sample = expires-after: "1w6d23h19m57s"
							Type:     schema.TypeString,
							Computed: true,
						},
						"fingerprint": { // Sample = fingerprint: "b7e51a21658fc7f5b2686033d490e2450bd9e47318075967a3edcfcab0beefb7"
							Type:     schema.TypeString,
							Computed: true,
						},
						"invalid_after": { // Sample = invalid-after: "2023-11-20 19:37:38"
							Type:     schema.TypeString,
							Computed: true,
						},
						"invalid_before": { // Sample = invalid-before: "2023-10-06 19:37:38"
							Type:     schema.TypeString,
							Computed: true,
						},
						"issuer": { // Sample = issuer: "C=NL,S=Friesland,L=Burgum,CN=Tjibbes Personal Root CA"
							Type:     schema.TypeString,
							Computed: true,
						},
						"key_size": { // Sample = key-size: "4096"
							Type:     schema.TypeInt,
							Computed: true,
						},
						"key_type": { // Sample = key-type: "rsa"
							Type:     schema.TypeString,
							Computed: true,
						},
						"key_usage": { // Sample = key-usage: "digital-signature,content-commitment,key-encipherment,tls-server"
							Type:     schema.TypeString,
							Computed: true,
						},
						"locality": { // Sample = locality: "Melbourne"
							Type:     schema.TypeString,
							Computed: true,
						},
						"name": { // Sample = name: "home-arpa"
							Type:     schema.TypeString,
							Computed: true,
						},
						"organization": { // Sample = organization: "My Company"
							Type:     schema.TypeString,
							Computed: true,
						},
						"private_key": { // Sample = private-key: "true"
							Type:     schema.TypeBool,
							Computed: true,
						},
						"serial_number": { // Sample = serial-number: "2c0fa8a659aecd074e65221549f5bd1c4ca13b6b"
							Type:     schema.TypeString,
							Computed: true,
						},
						"skid": { // Sample = skid: "54aeb135f6a693162ea5937de8488d60a4995f8b"
							Type:     schema.TypeString,
							Computed: true,
						},
						"state": { // Sample = state: "Victoria"
							Type:     schema.TypeString,
							Computed: true,
						},
						"subject_alt_name": { // Sample = subject-alt-name: "DNS:home.arpa,DNS:*.home.arpa"
							Type:     schema.TypeString,
							Computed: true,
						},
						"trusted": { // Sample = trusted: "true"
							Type:     schema.TypeBool,
							Computed: true,
						},
						"unit": { // Sample = unit: "My Division"
							Type:     schema.TypeString,
							Computed: true,
						},

					},
				},
			},
		},
	}
}

func datasourceCertificatesRead(ctx context.Context, d *schema.ResourceData, m interface{}) diag.Diagnostics {
	s := DatasourceCertificates().Schema
	path := s[MetaResourcePath].Default.(string)

	res, err := ReadItemsFiltered(buildReadFilter(d.Get(KeyFilter).(map[string]interface{})), path, m.(Client))
	if err != nil {
		return diag.FromErr(err)
	}

	return MikrotikResourceDataToTerraformDatasource(res, "Certificates", s, d)
}
