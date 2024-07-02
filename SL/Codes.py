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

#PlanningLabels = { #matching labels
		#"20": "PAA",
		#"66": "PAP",
		#"67": "PAR",
		#"1005": "PAL"
	#}
#PlanningLabelKeys = set(PlanningLabels.keys())

#you could argue that GreenConstraints should just have one tag, and then that the conversion happens from the generic tag -> find specific constraint 'tag'/straight to section
#this makes sense, but in finding the generic tag we would (or could) have already exhausted the list to work out that the site needs this tag - e.g. we finally get to SSSI, realise it has that constraint, then it gets generic tag
#would be doubling up on work by converting generic tag -> content vs. specific tag -> content

GreenConstraints = { #matching constraints
		"Green Belt": "GRB",
		"Ancient Woodland": "ACW",
		"National Nature Reserves": "NNR",
		"RAMSAR": "RAMS",
		"Country Parks": "CTP",
		"SAC": "SAC",
		"Local Nature Reserves": "LNR",
		"Parks and Gardens": "PAG",
		"National Parks": "NTP",
		"Designated Open Space": "DOS",
		"SPA 400m Buffer": "S4B",
		"Nutrient Neutrality": "NEU",
		"AONB": "AONB",
		"Conservation Area": "CVA",
		"Built Up Areas": "BUA",
		"SSSI Impact Zone": "SSSI"
	}
GreenConstraintKeys = set(GreenConstraints.keys())

HeritageConstraints = { #matching constraints
		"Battlefields": "BTF",
		"World Heritage Sites": "WHS",
		"Scheduled Monuments": "SDM",
		"Listed Building(s) in plot": "LBIP",
		"Listed Building(s) 50m Buffer": "LB50B"
	}
HeritageConstraintKeys = set(HeritageConstraints.keys())

FloodConstraints = { #matching constraints
		"Flood Zone 2": "FZ2",
		"Flood Zone 3": "FZ3"
	}
FloodConstraintKeys = set(FloodConstraints.keys())

GeneralConstraints = { #matching constraints
		"Fissure and Breaklines": "FAB",
		"Surface Mining": "SFM",
		"Town Centre Boundaries": "TCB",
		"Past Shallow Coal Mine Workings": "PASCMW",
		"North East Mining Groundwater Constraints": "NEMGC",
		"Mine Entry Potential Zone of Influence": "MEPZI",
		"Coal Outcrop": "COC",
		"Probable Shallow Coal Mine Workings": "PRSCMW",
		"Coal & Mining Development High Risk Area": "CMDHRA",
		"Surface Coal Resource Area": "SCRA",
		"Abandoned Mine": "ABDM",
		"Mining Reporting Area": "MRA"
	}
GeneralConstraintKeys = set(GeneralConstraints.keys())

LondonConstraints = { #matching constraints
		"Central Activities Zone": "CAZ",
		"LSIS": "LSIS",
		"SIL": "SIL"
	}
LondonConstraintKeys = set(LondonConstraints.keys())

LondonOpportunities = { #matching constraints
		"Housing Zones": "HSZ",
		"Opportunity Areas": "OPA",
		"Areas of Intensification": "AOI"
	}
LondonOpportunityKeys = set(LondonOpportunities.keys())

DevelopmentOpportunities = { #matching labels
		"infill": "IFL",
		"class_q": "CQ",
		"class_ma": "CMA"
	}
DevelopmentOpportunityKeys = set(DevelopmentOpportunities.keys())

#LNTSizeDictionary
