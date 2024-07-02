#This project mimics the function of the code generator, but requires a lot less manual input data (just template + land category) thanks to various APIs
#Future functionality to include an automatic sophistication detection for each individual site depending on LO - depending on how many sophistications, there will then be that many copies of extra 'Sections' and 'Templates' files
#Can't implement this now since SL does not provide private owner details through API (even if you wanted to buy the title/had already bought it)

import sys
import requests
import Codes
import Templates
import Sections
import APIs

LondonPostcodeDistricts = {
			"E", "EC", "N", "NW", "SE", "SW", "W", "WC"
		}

def AskForTag(Tag):
	while True:
		Inclusion = input(f"\nShould it be relevant to the site in question, would you like to include a tag about {Tag}? (Yes/No): ")
		if Inclusion == "Yes":
			print("\nGreat, we will include the tag only if it is relevant. This will only generate the corresponding letter content if such a placeholder appears in the chosen template (otherwise the tag is effectively irrelevant).\n")
			return Inclusion
		elif Inclusion == "No":
			return Inclusion
		else:
			print("\nInvalid input.")

def GenerateTags(TemplateCode, LandCategoryCode):
	
	#The multiple letter case sees the removal of London and LPA dependent yes/no questions - this is because we would need to check that every site wasn't in London and every site didn't have an LPA to rule out actually asking these questions - seems like a waste of time to implement
	
	#Assume no optional tags to begin with
	LeaseholderCode = ''
	PlanningCode = ''
	DevelopmentOpportunityCode = ''
	LocalOpportunityCode = ''
	LondonOpportunityCode = ''
	LondonConstraintCode = ''
	GreenConstraintCode = ''
	FloodConstraintCode = ''
	HeritageConstraintCode = ''
	GeneralConstraintCode = ''

	if LeaseholderDesire == "Yes": #include LeaseholderCode if applicable
		TitleClass = DealDetails.get('81892eef8bd7513f88a84638265e185f08b3078a') #Title Class key here
		if TitleClass == "leasehold":
			LeaseholderCode = "LPY"

	Labels = DealDetails.get('label') #Labels key here
	LabelsList = Labels.split(',')
	LabelSet = set(LabelsList)

	if PlanningDesire == "Yes": #include PlanningCode if applicable (if so, which?)
		PIntersection = Codes.PlanningLabelKeys & LabelSet
		if PIntersection:
			for key in Codes.PlanningLabels: #this construct technically isn't needed because this is the 'mutually exclusive' case, but I keep it the same as 'non-mutually exclusive' for consistency
				if key in PIntersection:
					single_planning_label = key
					PlanningCode = Codes.PlanningLabels[single_planning_label]
					break
			
	if DevelopmentOpportunityDesire == "Yes": #include DevelopmentOpportunityCode if applicable (if so, which?)
		DOIntersection = Codes.DevelopmentOpportunityKeys & LabelSet
		if DOIntersection:
			for key in Codes.DevelopmentOpportunities:
				if key in DOIntersection:
					single_development_label = key
					DevelopmentOpportunityCode = Codes.DevelopmentOpportunities[single_development_label]
					break
	
	if LPADetails:
		if LocalOpportunityDesire == "Yes": #check each Local Opportunity potential in priority order
			CFS = LPADetails.get('cdd1486d583005b9639280aee2bad932857420c7') #Call for Sites key here
			FiveYHLS = LPADetails.get('f2e117864e6d0efef3575ca192321d8ba4f55f28') #5YHLS Pass/Fail key here
			Consequence = LPADetails.get('acb2cab39dcdd362caadd8596fc1870ed0df0da7') #Consequence key here
			if CFS == "1002": #Open, Closed key is 1003
				LocalOpportunityCode = "CFS"
			elif FiveYHLS == "991": #Fail key
				LocalOpportunityCode = "HSNM"
			elif Consequence == "994": #Presumption key
				LocalOpportunityCode = "PSUMP"
			elif Consequence == "995": #Buffer + Action Plan key
				LocalOpportunityCode = "BAP"
			elif Consequence == "1000": #Action Plan key
				LocalOpportunityCode = "AP"

	Constraints = DealDetails.get('8bad9f73145375a568e94216e2ae349b96e86333') #Constraints key here
	ConstraintsList = Constraints.split(',')
	ConstraintListSet = set(ConstraintsList)
	
	#only bother checking London opportunities and constraints if site in London - no effect on user view of proceedings
	if TitlePostcodeFormatted:
		PostcodePrefix = TitlePostcodeFormatted[:2] if TitlePostcodeFormatted[1].isalpha() else TitlePostcodeFormatted[:1]
		if PostcodePrefix in LondonPostcodeDistricts:
			if LondonOpportunityDesire == "Yes": #check each London Opportunity potential in priority order
				LOIntersection = Codes.LondonOpportunityKeys & ConstraintListSet
				if LOIntersection:
					for key in Codes.LondonOpportunities:
						if key in LOIntersection:
							single_london_opportunity = key
							LondonOpportunityCode = Codes.LondonOpportunities[single_london_opportunity]
							break

			if LondonConstraintDesire == "Yes": #check each London Constraint potential in priority order
				LCIntersection = Codes.LondonConstraintKeys & ConstraintListSet
				if LCIntersection:
					for key in Codes.LondonConstraints:
						if key in LCIntersection:
							single_london_constraint = key
							LondonConstraintCode = Codes.LondonConstraints[single_london_constraint]
							break

	if GreenConstraintDesire == "Yes": #check each Green Constraint potential in priority order
		GCIntersection = Codes.GreenConstraintKeys & ConstraintListSet
		if GCIntersection:
			for key in Codes.GreenConstraints:
				if key in GCIntersection:
					single_green_constraint = key
					GreenConstraintCode = Codes.GreenConstraints[single_green_constraint]
					break
					
	if FloodConstraintDesire == "Yes": #check each Flood Constraint potential in priority order
		FCIntersection = Codes.FloodConstraintKeys & ConstraintListSet
		if FCIntersection:
			for key in Codes.FloodConstraints:
				if key in FCIntersection:
					single_flood_constraint = key
					FloodConstraintCode = Codes.FloodConstraints[single_flood_constraint]
					break
	
	if HeritageConstraintDesire == "Yes": #check each Heritage Constraint potential in priority order
		HCIntersection = Codes.HeritageConstraintKeys & ConstraintListSet
		if HCIntersection:
			for key in Codes.HeritageConstraints:
				if key in HCIntersection:
					single_heritage_constraint = key
					HeritageConstraintCode = Codes.HeritageConstraints[single_heritage_constraint]
					break
	
	if GeneralConstraintDesire == "Yes": #check each General Constraint potential in priority order
		GCIntersection = Codes.GeneralConstraintKeys & ConstraintListSet
		if GCIntersection:
			for key in Codes.GeneralConstraints:
				if key in GCIntersection:
					single_general_constraint = key
					GeneralConstraintCode = Codes.GeneralConstraints[single_general_constraint]
					break

	AllCodes = [TemplateCode, LeaseholderCode, PlanningCode, DevelopmentOpportunityCode, LocalOpportunityCode, LondonOpportunityCode, LondonConstraintCode, GreenConstraintCode, FloodConstraintCode, HeritageConstraintCode, GeneralConstraintCode, LandCategoryCode] #outer 2 from input, inner 10 (8 if not London) from above
	CodeFormatted = '-'.join([Code for Code in AllCodes if Code])
	print("\nSite Tags:", CodeFormatted)
	return CodeFormatted

def GenerateLetter(CodeFormatted, Salutation):
	
	AllCodes = CodeFormatted.split('-') #split up the site tags
	
	TemplateCode = AllCodes.pop(0) #get template code
	if MailingStatus == "I":
		ChosenTemplate = Templates.Initial[TemplateCode]
	elif MailingStatus == "FU1":
		ChosenTemplate = Templates.FU1[TemplateCode]
	else: #due to thorough logic, conclude this means Mailing Status is FU2
		ChosenTemplate = Templates.FU2[TemplateCode]
		
	LPANameFormatted = ''
	Road = ''
	TrainStation = ''
	TrainDistance = ''
	LNTSizeSection = ''
	Substation = ''
	NCA = ''
	
	SectionValues = { #Assume no optional content exists to begin with - this construction avoids having to use locals() to dynamically create e.g. 'LeaseholderSection' in a moment
		"LeaseholderSection": '',
		"PlanningSection": '',
		"DevelopmentOpportunitiesSection": '',
		"LocalOpportunitiesSection": '',
		"LondonOpportunitiesSection": '',
		"LondonConstraintsSection": '',
		"GreenConstraintsSection": '',
		"FloodConstraintsSection": '',
		"HeritageConstraintsSection": '',
		"GeneralConstraintsSection": ''
	}
	PossibleSections = ['Leaseholder', 'Planning', 'DevelopmentOpportunities', 'LocalOpportunities', 'LondonOpportunities', 'LondonConstraints', 'GreenConstraints', 'FloodConstraints', 'HeritageConstraints', 'GeneralConstraints']
	for i, section_name in enumerate(PossibleSections): #loops through all potential codes and gets the relevant content to feed into the relevant '...Section' variable
		if AllCodes: #this will still pointlessly loop through the last compulsory code (land category) - we'll cheat and get this content directly from LandCategory above
			NextCode = AllCodes.pop(0)
			NextSection = getattr(Sections, section_name)
			if NextCode in NextSection:
				SectionValues[f'{section_name}Section'] = NextSection[NextCode] #dynamically choose dictionary value to replace if applicable

	if LPADetails:
		LPAName = LPADetails.get('name') #LPA Name key here
		LPANameFormatted = LPAName.replace(" LPA", '')

	SiteName = DealDetails.get('title') #Title name key here
	TitleNumber = DealDetails.get('c78a4fb3140ed97b014b8378291177666df3ff9b') #Title number key here
	LandSize = DealDetails.get('0edab77e3bf453d6ee1387f05815b9de4b36428b') #Title size key here
	
	if LandSize is not None:
		if LandSize < 2:
			LNTSizeSection = "I believe your land parcel is suitable in part because it fits within LNT's sweet spot of between 1.3 and 2 acres."
		else:
			LNTSizeSection = "LNT's sweet spot is between 1.3 and 2 acres in size, and must be a particular shape. Would you be interested in the sale of a proportion of your land?"
	
	#Crystal Roof + VL API
	if TitlePostcodeFormatted:
		RoadURL = f"https://crystalroof.co.uk/customer-api/transport/closest-roads/v1/{TitlePostcodeFormatted}"
		response = requests.get(RoadURL, params = APIs.CR_query_params)
		if response.status_code == 200:
			RoadDetails = response.json().get('data', {})
			Motorway = RoadDetails.get('motorway', {}).get('roadNumber') #e.g. M3
			MotorwayProximity = RoadDetails.get('motorway', {}).get('distance') #in metres
			ARoad = RoadDetails.get('aRoad', {}).get('roadNumber') #e.g. A240
			ARoadProximity = RoadDetails.get('aRoad', {}).get('distance') #in metres
			if MotorwayProximity < ARoadProximity: #take closest road out of M or A types
				Road = Motorway
			else:
				Road = ARoad
		else:
			print("\nFor your information, we couldn't find the closest main road to the title postcode. The site tag and letter will generate below as usual.")
		PostcodePrefix = TitlePostcodeFormatted[:2] if TitlePostcodeFormatted[1].isalpha() else TitlePostcodeFormatted[:1]
		if PostcodePrefix in LondonPostcodeDistricts:
			TrainURL = f"https://crystalroof.co.uk/customer-api/transport/closest-london-transport-stations/v1/{TitlePostcodeFormatted}"
		else:
			TrainURL = f"https://crystalroof.co.uk/customer-api/transport/closest-rail-stations/v1/{TitlePostcodeFormatted}"
		response = requests.get(TrainURL, params = APIs.CR_query_params)
		if response.status_code == 200:
			TrainDetails = response.json().get('data', [])
			TrainStation = TrainDetails[0].get('name')
			TrainDistance = round(TrainDetails[0].get('distance'))
		else:
			print("\nFor your information, we couldn't find the closest train station to the title postcode. The site tag and letter will generate below as usual.")
		SubstationURL = f"https://vbwsm50jpc.execute-api.eu-west-2.amazonaws.com/v1/substation?titlePostcode={TitlePostcodeFormatted}"
		response = requests.get(SubstationURL, headers = APIs.VL_headers)
		if response.status_code == 200:
			SubstationDetails = response.json().get('data', {})
			Substation = SubstationDetails.get('closest_substation')
		else:
			print("\nFor your information, we couldn't find the closest substation to the title postcode. The site tag and letter will generate below as usual.")
		NCAURL = f"https://vbwsm50jpc.execute-api.eu-west-2.amazonaws.com/v1/nca?titlePostcode={TitlePostcodeFormatted}"
		response = requests.get(NCAURL, headers = APIs.VL_headers)
		if response.status_code == 200:
			NCADetails = response.json().get('data', {})
			if NCADetails:
				NCA = NCADetails.get('national_character_area')
			else:
				print("\nFor your information, we couldn't find the NCA for the title postcode. The site tag and letter will generate below as usual.")
		else:
			print("\nFor your information, we couldn't find the NCA for the title postcode. The site tag and letter will generate below as usual.")
	
	ChosenTemplate = ChosenTemplate.replace("[LeaseholderSection]", SectionValues["LeaseholderSection"])
	ChosenTemplate = ChosenTemplate.replace("[PlanningSection]", SectionValues["PlanningSection"])
	ChosenTemplate = ChosenTemplate.replace("[DevelopmentOpportunitiesSection]", SectionValues["DevelopmentOpportunitiesSection"])
	ChosenTemplate = ChosenTemplate.replace("[LocalOpportunitiesSection]", SectionValues["LocalOpportunitiesSection"])
	ChosenTemplate = ChosenTemplate.replace("[LondonOpportunitiesSection]", SectionValues["LondonOpportunitiesSection"])
	ChosenTemplate = ChosenTemplate.replace("[LondonConstraintsSection]", SectionValues["LondonConstraintsSection"])
	ChosenTemplate = ChosenTemplate.replace("[GreenConstraintsSection]", SectionValues["GreenConstraintsSection"])
	ChosenTemplate = ChosenTemplate.replace("[FloodConstraintsSection]", SectionValues["FloodConstraintsSection"])
	ChosenTemplate = ChosenTemplate.replace("[HeritageConstraintsSection]", SectionValues["HeritageConstraintsSection"])
	ChosenTemplate = ChosenTemplate.replace("[GeneralConstraintsSection]", SectionValues["GeneralConstraintsSection"])
	ChosenTemplate = ChosenTemplate.replace("[LNTSizeSection]", LNTSizeSection)
	
	ChosenTemplate = ChosenTemplate.replace("[InitialDate]", InitialDate)
	ChosenTemplate = ChosenTemplate.replace("[FUDate]", FUDate)
	
	ChosenTemplate = ChosenTemplate.replace("[SiteName]", SiteName)
	ChosenTemplate = ChosenTemplate.replace("[TitleNumber]", TitleNumber)
	ChosenTemplate = ChosenTemplate.replace("[Road]", Road)
	ChosenTemplate = ChosenTemplate.replace("[TrainStation]", TrainStation)
	ChosenTemplate = ChosenTemplate.replace("[TrainDistance]", TrainDistance)
	ChosenTemplate = ChosenTemplate.replace("[Substation]", Substation)
	ChosenTemplate = ChosenTemplate.replace("[NCA]", NCA)
	ChosenTemplate = ChosenTemplate.replace("[LandCategory]", LandCategory.lower()) #make lowercase
	ChosenTemplate = ChosenTemplate.replace("[LPANameFormatted]", LPANameFormatted)
	ChosenTemplate = ChosenTemplate.replace("[Email]", Email)
	ChosenTemplate = ChosenTemplate.replace("[Salutation]", Salutation)
	
	print("\n\nLetter:")
	print('\n\n', ChosenTemplate)
	return ChosenTemplate

IDs = input("Enter Deal IDs - they should be comma-space separated (for example: 1234, 56789): ")
IDsFormatted = IDs.split(',')
IDArray = [ID.strip() for ID in IDsFormatted]

print("\nHere are the Template options:\n")
for keys, value in Codes.Templates.items():
	print(keys)

while True:
	Template = input("\nEnter Template (case sensitive): ")
	if Codes.Templates.get(Template, None):
		TemplateCode = Codes.Templates[Template]
		break
	else:
		print("\nInvalid input. Do the templates for this client exist?")

LandCategoryCodes = []

print("\nHere are the Land Category options:\n")
for keys, value in Codes.LandCategories.items():
	print(keys)

while True:
	LandCategories = input("\nEnter Site Land Categories - they should be comma-space separated in the exact same manner and correspond to the above IDs: ")
	LandCategoriesFormatted = LandCategories.split(',')
	LandCategoryArray = [LandCategory.strip() for LandCategory in LandCategoriesFormatted]
	if len(LandCategoryArray) != len(IDArray):
		print("\nThe number of land categories you have provided do not match the number of deal IDs provided. Please try again.\n")
		continue #skip the remaining code of this iteration
	exitAllowed = True
	for LandCategory in LandCategoryArray:
		if LandCategory not in Codes.LandCategories:
			exitAllowed = False
			print("\nOne of the land categories was entered wrong. Please try again - make sure you capitalise and make no spelling errors.\n")
			break
		LandCategoryCode = Codes.LandCategories[LandCategory]
		LandCategoryCodes.append(LandCategoryCode)
	if exitAllowed:
		break

LeaseholderDesire = AskForTag("a leaseholder")
PlanningDesire = AskForTag("a planning application on the title")
DevelopmentOpportunityDesire = AskForTag("a permitted development opportunity (e.g. Class Q)")
LocalOpportunityDesire = AskForTag("an opportunity in the LPA (e.g. open call for sites)")
LondonOpportunityDesire = AskForTag("a London opportunity (e.g. Opportunity Area)")
LondonConstraintDesire = AskForTag("a London constraint")
GreenConstraintDesire = AskForTag("a green constraint (e.g. Green Belt)")
FloodConstraintDesire = AskForTag("a flood constraint (Flood Zone 2/3)")
HeritageConstraintDesire = AskForTag("a heritage constraint (e.g. Listed Building(s) In Plot)")
GeneralConstraintDesire = AskForTag("a general constraint (i.e. mining or coal related)")

SiteTagArray = []

for ID, LandCategoryCode in zip(IDArray, LandCategoryCodes):
	
	#PD API
	DealDetailsURL = f"https://api.pipedrive.com/v1/deals/{ID}"
	response = requests.get(DealDetailsURL, params = APIs.PD_query_params)
	if response.status_code == 200:
		DealDetails = response.json().get('data', {})
		TitlePostcode = DealDetails.get('6518beb59dfa14c5c5f38a819924bf7eaee92157') #Title Postcode key here - None by default if no Title Postcode found
		TitlePostcodeFormatted = None
		if TitlePostcode is not None:
			TitlePostcodeFormatted = TitlePostcode.replace(" ","") #remove any spaces from postcode
		else:
			print(f"\nFor your information, we couldn't find any Title Postcode on PipeDrive for deal ID {ID}, so we couldn't gauge metrics such as the closest main road or where the site is exactly. The site tags and letters will generate below as usual.")
	else:
		sys.exit(f"Couldn't find this site in PipeDrive (deal ID {ID}).")

	#PD API
	try:
		LPAid = DealDetails.get('824290f62e26f62549d92447ca6fca636c223c2a', {}).get('value') #LPA ID key here
		LPADetailsURL = f"https://api.pipedrive.com/v1/organizations/{LPAid}"
		response = requests.get(LPADetailsURL, params = APIs.PD_query_params)
		if response.status_code == 200:
			LPADetails = response.json().get('data', {})
		else:
			print("\nFor your information, we couldn't find any Linked LPA on PipeDrive, so we couldn't examine any local opportunities. The site tag and letter will generate below as usual.")
	except:
		LPADetails = None
		print("\nFor your information, we couldn't find any Linked LPA on PipeDrive, so we couldn't examine any local opportunities. The site tag and letter will generate below as usual.")

	CodeFormatted = GenerateTags(TemplateCode, LandCategoryCode)
	SiteTagArray.append(CodeFormatted)

InitialDate = ''
FUDate = ''

while True: #check initial/follow up 1/follow up 2 and pick correct template dictionary to get value from
	InitialStatus = input("\nIs this an initial mailing? Type 'Yes' or 'No': ")
	if InitialStatus == "Yes":
		MailingStatus = "I"
		break
	elif InitialStatus == "No":
		while True:
			InitialDate = input("\nWhen did you send the initial letters? For example, 'Monday 1st January 2024': ")
			FollowUpStatus = input("\nIs this follow up 1 or 2? Type '1' or '2': ")
			if FollowUpStatus == '1':
				MailingStatus = "FU1"
				break
			elif FollowUpStatus == '2':
				FUDate = input("\nWhen did you send the first follow up letters? Same date format as above, please: ")
				MailingStatus = "FU2"
				break
			else:
				print("\nInvalid input.")
		break
	else:
		print("\nInvalid input.")

Salutations = {
		"Dan": "Daniel Robinson\nManaging Director, VirginLand",
		"Charlie": "Charles Youngs\nLand Director, VirginLand"
	}

Emails = {
		"Dan": "daniel@virginland.com",
		"Charlie": "charles@virginland.com"
	}

while True:
	Association = input("\nWould you like these letters to be associated with Dan or Charlie? Type either name: ")
	if Salutations.get(Association, None): #implies valid for Emails also
		Salutation = Salutations[Association]
		Email = Emails[Association]
		break
	else:
		print("\nInvalid input.")
	
for ID, CodeFormatted in zip(IDArray, SiteTagArray):
	
	#Aware below two PD API sections are a duplicate of the other for loop but this was the most pain-free way I could see of listing all tags, followed by all letters (instead of 1-1, 2-2, etc.)
	
	#PD API
	DealDetailsURL = f"https://api.pipedrive.com/v1/deals/{ID}"
	response = requests.get(DealDetailsURL, params = APIs.PD_query_params)
	if response.status_code == 200:
		DealDetails = response.json().get('data', {})
		TitlePostcode = DealDetails.get('6518beb59dfa14c5c5f38a819924bf7eaee92157') #Title Postcode key here - None by default if no Title Postcode found
		if TitlePostcode is not None:
			TitlePostcodeFormatted = TitlePostcode.replace(" ","") #remove any spaces from postcode
		else:
			print(f"\nFor your information, we couldn't find any Title Postcode on PipeDrive for deal ID {ID}, so we couldn't gauge metrics such as the closest main road or where the site is exactly. The site tags and letters will generate below as usual.")
	else:
		sys.exit(f"Couldn't find this site in PipeDrive (deal ID {ID}).")

	#PD API
	try:
		LPAid = DealDetails.get('824290f62e26f62549d92447ca6fca636c223c2a', {}).get('value') #LPA ID key here
		LPADetailsURL = f"https://api.pipedrive.com/v1/organizations/{LPAid}"
		response = requests.get(LPADetailsURL, params = APIs.PD_query_params)
		if response.status_code == 200:
			LPADetails = response.json().get('data', {})
		else:
			print("\nFor your information, we couldn't find any Linked LPA on PipeDrive, so we couldn't examine any local opportunities. The site tag and letter will generate below as usual.")
	except:
		LPADetails = None
		print("\nFor your information, we couldn't find any Linked LPA on PipeDrive, so we couldn't examine any local opportunities. The site tag and letter will generate below as usual.")	
			
	GenerateLetter(CodeFormatted, Salutation)
