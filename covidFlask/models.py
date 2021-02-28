'''
CovidCasus
{
	"_id"                 : ObjectId("6028574b09095c1b022c3086"),
	"datum"               : ISODate("2021-02-13T10:00:00Z"),
	"publicatie"          : ISODate("2021-01-01T00:00:00Z"),
	"stat_type"           : "DOO",
	"leeftijd_grp"        : 49,
	"geslacht"            : "V",
	"provincie"           : "Drenthe",
	"ziekenhuis"          : false,
	"overleden"           : false,
	"week_van_overlijden" : "",
	"gem_service"         : "GGD Drenthe"
}

CovidCol
{
	"_id"          : ObjectId("600dab0ce39bada54078118a"),
	"datum"        : ISODate("2021-01-24T10:00:00Z"),
	"publicatie"   : ISODate("2021-01-01T00:00:00Z"),
	"gem_code"     : "GM0014",
	"gem_naam"     : "Groningen",
	"provincie"    : "Groningen",
	"sec_reg_code" : "VR01",
	"sec_reg_naam" : "Groningen",
	"gem_service"  : "GGD Groningen",
	"roaz_reg"     : "Acute Zorgnetwerk Noord Nederland",
	"tot_reported" : 69,
	"opnames"      : 1,
	"overleden"    : 1
}

Gemeentes
{
	"_id" : ObjectId("600ca8a51ba06e9fe2ebca64"),
	"provincie" : "Groningen",
	"gemeente"  : "Groningen",
	"inwoners"  : 231112
}

Testen
{
    "_id"          : ObjectId("600ca8a51ba06e9fe2ebca64"),
    "datum"        : ISODate("2021-01-24T10:00:00Z"),
	"publicatie"   : ISODate("2021-01-01T00:00:00Z"),
    "sec_reg_code" : "VR01",
	"sec_reg_naam" : "Groningen",
    "test_tot"     : 100,
    "test_pos"     : 10
}

'''