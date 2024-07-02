import tkinter as tk
from tkinter import messagebox
import requests
import Codes
import Templates
import Sections
import APIs

Salutations = {
    "Dan": "Daniel Robinson\nManaging Director, VirginLand",
    "Charlie": "Charles Youngs\nLand Director, VirginLand"
}

Emails = {
    "Dan": "daniel@virginland.com",
    "Charlie": "charles@virginland.com"
}

LondonPostcodeDistricts = {
			"E", "EC", "N", "NW", "SE", "SW", "W", "WC"
		}

# Function to ask for tags
def AskForTag(Tag):
    response = messagebox.askquestion("Tag Inclusion", f"Should it be relevant to the site in question, would you like to include a tag about {Tag}?")
    return "Yes" if response == 'yes' else "No"

# Function to generate tags
def GenerateTags(TemplateCode, LandCategoryCode):
    #Assume no optional tags to begin with
	LeaseholderCode = ''
	DevelopmentOpportunityCode = ''
	LocalOpportunityCode = ''
	LondonOpportunityCode = ''
	LondonConstraintCode = ''
	GreenConstraintCode = ''
	FloodConstraintCode = ''
	HeritageConstraintCode = ''
	GeneralConstraintCode = ''

	LeaseholderDesire = AskForTag("a leaseholder")
	if LeaseholderDesire == "Yes": #include LeaseholderCode if applicable
		TitleClass = TitleDetails.get('calculated_class_of_title') #Title Class key here
		if TitleClass == "leasehold":
			LeaseholderCode = "LPY"

	#omitting since SL API really isn't helpful when it comes to identifying planning apps on a title
	#PlanningDesire = AskForTag("a planning application on the title")
	#if PlanningDesire == "Yes": #include PlanningCode if applicable (if so, which?)
		#PIntersection = Codes.PlanningLabelKeys & LabelSet
		#if PIntersection:
			#for key in Codes.PlanningLabels: #this construct technically isn't needed because this is the 'mutually exclusive' case, but I keep it the same as 'non-mutually exclusive' for consistency
				#if key in PIntersection:
					#single_planning_label = key
					#PlanningCode = Codes.PlanningLabels[single_planning_label]
					#break
			
	DevelopmentOpportunityDesire = AskForTag("a permitted development opportunity (e.g. Class Q)")
	if DevelopmentOpportunityDesire == "Yes": #include DevelopmentOpportunityCode if applicable (if so, which?)
		DevelopmentOpportunities = TitleDetails.get('development_opportunities', [])
		if DevelopmentOpportunities:
			Opportunity = DevelopmentOpportunities[0]
			if Opportunity in Codes.DevelopmentOpportunities:
				DevelopmentOpportunityCode = Codes.DevelopmentOpportunities[Opportunity]
	
	#only ask about local opportunities if Linked LPA was found
	if LPADetails:
		LocalOpportunityDesire = AskForTag("an opportunity in the LPA (e.g. open call for sites)")
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
	
	Constraints = TitleDetails.get('constraints', []) #Constraints key here
	ConstraintListSet = set(Constraints)
	
	#only ask about London opportunities and constraints if site in London - only if TitlePostcodeFormatted exists (see above)
	if TitlePostcodeFormatted:
		PostcodePrefix = TitlePostcodeFormatted[:2] if TitlePostcodeFormatted[1].isalpha() else TitlePostcodeFormatted[:1]
		if PostcodePrefix in LondonPostcodeDistricts:
			LondonOpportunityDesire = AskForTag("a London opportunity (e.g. Opportunity Area)")
			if LondonOpportunityDesire == "Yes": #check each London Opportunity potential in priority order
				LOIntersection = Codes.LondonOpportunityKeys & ConstraintListSet
				if LOIntersection:
					for key in Codes.LondonOpportunities:
						if key in LOIntersection:
							single_london_opportunity = key
							LondonOpportunityCode = Codes.LondonOpportunities[single_london_opportunity]
							break

			LondonConstraintDesire = AskForTag("a London constraint")
			if LondonConstraintDesire == "Yes": #check each London Constraint potential in priority order
				LCIntersection = Codes.LondonConstraintKeys & ConstraintListSet
				if LCIntersection:
					for key in Codes.LondonConstraints:
						if key in LCIntersection:
							single_london_constraint = key
							LondonConstraintCode = Codes.LondonConstraints[single_london_constraint]
							break

	GreenConstraintDesire = AskForTag("a green constraint (e.g. Green Belt)")
	if GreenConstraintDesire == "Yes": #check each Green Constraint potential in priority order
		GCIntersection = Codes.GreenConstraintKeys & ConstraintListSet
		if GCIntersection:
			for key in Codes.GreenConstraints:
				if key in GCIntersection:
					single_green_constraint = key
					GreenConstraintCode = Codes.GreenConstraints[single_green_constraint]
					break
					
	FloodConstraintDesire = AskForTag("a flood constraint (Flood Zone 2/3)")
	if FloodConstraintDesire == "Yes": #check each Flood Constraint potential in priority order
		FCIntersection = Codes.FloodConstraintKeys & ConstraintListSet
		if FCIntersection:
			for key in Codes.FloodConstraints:
				if key in FCIntersection:
					single_flood_constraint = key
					FloodConstraintCode = Codes.FloodConstraints[single_flood_constraint]
					break
	
	HeritageConstraintDesire = AskForTag("a heritage constraint (e.g. Listed Building(s) In Plot)")
	if HeritageConstraintDesire == "Yes": #check each Heritage Constraint potential in priority order
		HCIntersection = Codes.HeritageConstraintKeys & ConstraintListSet
		if HCIntersection:
			for key in Codes.HeritageConstraints:
				if key in HCIntersection:
					single_heritage_constraint = key
					HeritageConstraintCode = Codes.HeritageConstraints[single_heritage_constraint]
					break
	
	GeneralConstraintDesire = AskForTag("a general constraint (i.e. mining or coal related)")
	if GeneralConstraintDesire == "Yes": #check each General Constraint potential in priority order
		GCIntersection = Codes.GeneralConstraintKeys & ConstraintListSet
		if GCIntersection:
			for key in Codes.GeneralConstraints:
				if key in GCIntersection:
					single_general_constraint = key
					GeneralConstraintCode = Codes.GeneralConstraints[single_general_constraint]
					break

	AllCodes = [TemplateCode, LeaseholderCode, DevelopmentOpportunityCode, LocalOpportunityCode, LondonOpportunityCode, LondonConstraintCode, GreenConstraintCode, FloodConstraintCode, HeritageConstraintCode, GeneralConstraintCode, LandCategoryCode] #outer 2 from input, inner 10 (8 if not London) from above
	CodeFormatted = '-'.join([Code for Code in AllCodes if Code])
	return CodeFormatted

# Function to generate the letter
def GenerateLetter(TitleNumber, LPANameFormatted, CodeFormatted, Salutation):
	AllCodes = CodeFormatted.split('-') #split up the site tags
	
	TemplateCode = AllCodes.pop(0) #get template code
	if MailingStatus == "I":
		ChosenTemplate = Templates.Initial[TemplateCode]
	elif MailingStatus == "FU1":
		ChosenTemplate = Templates.FU1[TemplateCode]
	else: #due to thorough logic, conclude this means Mailing Status is FU2
		ChosenTemplate = Templates.FU2[TemplateCode]
	
	Road = ''
	TrainStation = ''
	TrainDistance = ''
	LNTSizeSection = ''
	Substation = ''
	NCA = ''
	
	SectionValues = { #Assume no optional content exists to begin with - this construction avoids having to use locals() to dynamically create e.g. 'LeaseholderSection' in a moment
		"LeaseholderSection": '',
		"DevelopmentOpportunitiesSection": '',
		"LocalOpportunitiesSection": '',
		"LondonOpportunitiesSection": '',
		"LondonConstraintsSection": '',
		"GreenConstraintsSection": '',
		"FloodConstraintsSection": '',
		"HeritageConstraintsSection": '',
		"GeneralConstraintsSection": ''
	}
	PossibleSections = ['Leaseholder', 'DevelopmentOpportunities', 'LocalOpportunities', 'LondonOpportunities', 'LondonConstraints', 'GreenConstraints', 'FloodConstraints', 'HeritageConstraints', 'GeneralConstraints']
	for i, section_name in enumerate(PossibleSections): #loops through all potential codes and gets the relevant content to feed into the relevant '...Section' variable
		if AllCodes: #this will still pointlessly loop through the last compulsory code (land category) - we'll cheat and get this content directly from LandCategory above
			NextCode = AllCodes.pop(0)
			NextSection = getattr(Sections, section_name)
			if NextCode in NextSection:
				SectionValues[f'{section_name}Section'] = NextSection[NextCode] #dynamically choose variable to populate if applicable

	SiteName = TitleDetails.get('property_address') #Title name key here
	
	#Crystal Roof API
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
			TrainDistance = str(round(TrainDetails[0].get('distance')))
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
	ChosenTemplate = ChosenTemplate.replace("[DevelopmentOpportunitiesSection]", SectionValues["DevelopmentOpportunitiesSection"])
	ChosenTemplate = ChosenTemplate.replace("[LocalOpportunitiesSection]", SectionValues["LocalOpportunitiesSection"])
	ChosenTemplate = ChosenTemplate.replace("[LondonOpportunitiesSection]", SectionValues["LondonOpportunitiesSection"])
	ChosenTemplate = ChosenTemplate.replace("[LondonConstraintsSection]", SectionValues["LondonConstraintsSection"])
	ChosenTemplate = ChosenTemplate.replace("[GreenConstraintsSection]", SectionValues["GreenConstraintsSection"])
	ChosenTemplate = ChosenTemplate.replace("[FloodConstraintsSection]", SectionValues["FloodConstraintsSection"])
	ChosenTemplate = ChosenTemplate.replace("[HeritageConstraintsSection]", SectionValues["HeritageConstraintsSection"])
	ChosenTemplate = ChosenTemplate.replace("[GeneralConstraintsSection]", SectionValues["GeneralConstraintsSection"])
	
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
	
	return ChosenTemplate

# Function to run the main process
def run_main_process():
	global TitleDetails, LPADetails, TitlePostcodeFormatted, InitialDate, FUDate, MailingStatus, LandCategory, LandCategoryCode, Salutation, Email

	TitleNumber = title_number_entry.get()

	#SL API
	TitlePostcodeFormatted = None
	TitleDetailsURL = f"https://api.searchland.co.uk/v1/titles/get?titleNumber={TitleNumber}"
	response = requests.get(TitleDetailsURL, headers = APIs.SL_headers)
	if response.status_code == 200:
		TitleDetails = response.json().get('data', {})
		TitlePostcode = TitleDetails.get('postcode') #Title Postcode key here - None by default if no Title Postcode found
		if TitlePostcode is not None and TitlePostcode != "":
			TitlePostcodeFormatted = TitlePostcode.replace(" ","") #remove any spaces from postcode
		else:
			messagebox.showinfo("Information", "We couldn't find any Title Postcode on SearchLand, so we couldn't gauge metrics such as the closest main road or where the site is exactly, as well as failing to pinpoint its LPA and relevant local opportunities.")
	else:
		messagebox.showerror("Error", "Couldn't find this title on SearchLand.")
		return

    #PO + PD API - LPA workaround
	LPADetails = None
	LPANameFormatted = ''
	if TitlePostcodeFormatted: #only bother with LPA stuff if we actually have a postcode
		LPANameURL = f"https://api.postcodes.io/postcodes/{TitlePostcodeFormatted}"
		response = requests.get(LPANameURL)
		if response.status_code == 200:
			LPANameFormatted = response.json().get('result', {}).get('admin_district')
			LPAidURL = f"https://api.pipedrive.com/v1/organizations/search?term={LPANameFormatted}"
			response = requests.get(LPAidURL, params = APIs.PD_query_params)
			if response.status_code == 200:
				LPAid = response.json().get('data', {}).get('items', [{}])[0].get('item', {}).get('id') #slightly mad JSON structure
				LPADetailsURL = f"https://api.pipedrive.com/v1/organizations/{LPAid}"
				response = requests.get(LPADetailsURL, params = APIs.PD_query_params)
				if response.status_code == 200:
					LPADetails = response.json().get('data', {})
				else:
					messagebox.showinfo("Information", "We couldn't find the LPA from its ID on PipeDrive, so we couldn't examine any local opportunities.")
			else:
				messagebox.showinfo("Information", "We couldn't find the postcode's LPA on PipeDrive, so we couldn't examine any local opportunities.")
		else:
			messagebox.showinfo("Information", "We couldn't find this postcode on Postcodes.io, so we couldn't examine any local opportunities.")

	Template = template_var.get()
	TemplateCode = Codes.Templates.get(Template)

	LandCategory = land_category_var.get()
	LandCategoryCode = Codes.LandCategories.get(LandCategory)

	CodeFormatted = GenerateTags(TemplateCode, LandCategoryCode)
	code_text.delete(1.0, tk.END)
	code_text.insert(tk.END, CodeFormatted)

	InitialDate = ''
	FUDate = ''

	InitialStatus = initial_status_var.get()
	if InitialStatus == "Yes":
		MailingStatus = "I"
	else:
		InitialDate = initial_date_entry.get()
		FollowUpStatus = follow_up_status_var.get()
		if FollowUpStatus == '1':
			MailingStatus = "FU1"
		elif FollowUpStatus == '2':
			FUDate = follow_up_date_entry.get()
			MailingStatus = "FU2"

	Association = association_var.get()
	Salutation = Salutations[Association]
	Email = Emails[Association]
	
	letter = GenerateLetter(TitleNumber, LPANameFormatted, CodeFormatted, Salutation)
	output_text.delete(1.0, tk.END)
	output_text.insert(tk.END, letter)

# Initialize the main window
root = tk.Tk()
root.title("Site Tagging Software and Generation")

# Deal ID
title_number_label = tk.Label(root, text="Enter Title Number:")
title_number_label.pack()
title_number_entry = tk.Entry(root)
title_number_entry.pack()

# Template options
template_label = tk.Label(root, text="Template Options:")
template_label.pack()
template_var = tk.StringVar(root)
template_menu = tk.OptionMenu(root, template_var, *Codes.Templates.keys())
template_menu.pack()

# Land category options
land_category_label = tk.Label(root, text="Land Category Options:")
land_category_label.pack()
land_category_var = tk.StringVar(root)
land_category_menu = tk.OptionMenu(root, land_category_var, *Codes.LandCategories.keys())
land_category_menu.pack()

# Initial status
initial_status_label = tk.Label(root, text="Is this an initial mailing?")
initial_status_label.pack()
initial_status_var = tk.StringVar(root)
initial_status_menu = tk.OptionMenu(root, initial_status_var, "Yes", "No")
initial_status_menu.pack()

# Initial date and follow-up status
initial_date_label = tk.Label(root, text="When did you send the initial letter?")
initial_date_entry = tk.Entry(root)
follow_up_status_label = tk.Label(root, text="Is this follow up 1 or 2?")
follow_up_status_var = tk.StringVar(root)
follow_up_status_menu = tk.OptionMenu(root, follow_up_status_var, "1", "2")
follow_up_date_label = tk.Label(root, text="When did you send the first follow up letter?")
follow_up_date_entry = tk.Entry(root)

def update_follow_up_options(*args):
    if initial_status_var.get() == "No":
        initial_date_label.pack()
        initial_date_entry.pack()
        follow_up_status_label.pack()
        follow_up_status_menu.pack()
        follow_up_status_var.trace_add("write", update_follow_up_date)
    else:
        initial_date_label.pack_forget()
        initial_date_entry.pack_forget()
        follow_up_status_label.pack_forget()
        follow_up_status_menu.pack_forget()
        follow_up_date_label.pack_forget()
        follow_up_date_entry.pack_forget()

def update_follow_up_date(*args):
    if follow_up_status_var.get() == "2":
        follow_up_date_label.pack()
        follow_up_date_entry.pack()
    else:
        follow_up_date_label.pack_forget()
        follow_up_date_entry.pack_forget()

initial_status_var.trace_add("write", update_follow_up_options)

# Association options
association_label = tk.Label(root, text="Would you like this letter to be associated with Dan or Charlie?")
association_label.pack()
association_var = tk.StringVar(root)
association_menu = tk.OptionMenu(root, association_var, *Salutations.keys())
association_menu.pack()

# Run button
run_button = tk.Button(root, text="Generate Letter", command=run_main_process)
run_button.pack()

# Code text
code_text = tk.Text(root, height=5, width=100)
code_text.pack()

# Output text
output_text = tk.Text(root, height=20, width=100)
output_text.pack()

# Start the Tkinter event loop
root.mainloop()
