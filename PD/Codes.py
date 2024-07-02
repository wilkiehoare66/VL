LandCategories = {
		"Land": "LCL",
		"Garden": "LCG",
		"Property": "LCP",
		"Properties": "LCPS",
		"Garages": "LCGS",
		"Property and Associated Land": "DTPD",
		"Agricultural Barns": "LCAG",
		"Car Park": "LCCP",
		"Stables": "LCS"
	}
	
Templates = { #new template = new code required here for code to work (and obviously template content below - initial/FU1/FU2)
		"Biofarm": "BIO",
		"Electric Land": "EL",
		"Galliford Try Investments": "GTI",
		"GSE Truck Existing": "GSETE",
		"GSE Truck Greenfield": "GSETGF",
		"GRIDSERVE": "GRID",
		"LNT": "LNT",
		"Wates Developments": "WTS",
	}
	
PlanningLabels = { #matching labels
		"20": "PAA",
		"66": "PAP",
		"67": "PAR",
		"1005": "PAL"
	}
PlanningLabelKeys = set(PlanningLabels.keys())

#you could argue that GreenConstraints should just have one tag, and then that the conversion happens from the generic tag -> find specific constraint 'tag'/straight to section
#this makes sense, but in finding the generic tag we would (or could) have already exhausted the list to work out that the site needs this tag - e.g. we finally get to SSSI, realise it has that constraint, then it gets generic tag
#would be doubling up on work by converting generic tag -> content vs. specific tag -> content

GreenConstraints = { #matching constraints
		"625": "GRB",
		"640": "ACW",
		"656": "NNR",
		"654": "RAMS",
		"652": "CTP",
		"644": "SAC",
		"638": "LNR",
		"637": "PAG",
		"645": "NTP",
		"647": "DOS",
		"641": "S4B",
		"642": "NEU",
		"635": "AONB",
		"631": "CVA",
		"619": "BUA",
		"629": "SSSI"
	}
GreenConstraintKeys = set(GreenConstraints.keys())

HeritageConstraints = { #matching constraints
		"639": "BTF",
		"651": "WHS",
		"643": "SDM",
		"636": "LBIP",
		"627": "LB50B"
	}
HeritageConstraintKeys = set(HeritageConstraints.keys())

FloodConstraints = { #matching constraints
		"628": "FZ2",
		"630": "FZ3"
	}
FloodConstraintKeys = set(FloodConstraints.keys())

GeneralConstraints = { #matching constraints
		"655": "FAB",
		"634": "SFM",
		"646": "TCB",
		"622": "PASCMW",
		"632": "NEMGC",
		"633": "MEPZI",
		"624": "COC",
		"626": "PRSCMW",
		"620": "CMDHRA",
		"621": "SCRA",
		"618": "ABDM",
		"623": "MRA"
	}
GeneralConstraintKeys = set(GeneralConstraints.keys())

LondonConstraints = { #matching constraints
		"657": "CAZ",
		"648": "LSIS",
		"653": "SIL"
	}
LondonConstraintKeys = set(LondonConstraints.keys())

LondonOpportunities = { #matching constraints
		"649": "HSZ",
		"650": "OPA",
		"908": "AOI"
	}
LondonOpportunityKeys = set(LondonOpportunities.keys())

DevelopmentOpportunities = { #matching labels
		"599": "IFL",
		"600": "CQ",
		"601": "CMA"
	}
DevelopmentOpportunityKeys = set(DevelopmentOpportunities.keys())
