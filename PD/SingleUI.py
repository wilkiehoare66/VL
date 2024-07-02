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

    LeaseholderDesire = AskForTag("a leaseholder")
    if LeaseholderDesire == "Yes":
        TitleClass = DealDetails.get('81892eef8bd7513f88a84638265e185f08b3078a')
        if TitleClass == "leasehold":
            LeaseholderCode = "LPY"

    Labels = DealDetails.get('label')
    LabelsList = Labels.split(',')
    LabelSet = set(LabelsList)

    PlanningDesire = AskForTag("a planning application on the title")
    if PlanningDesire == "Yes":
        PIntersection = Codes.PlanningLabelKeys & LabelSet
        if PIntersection:
            for key in Codes.PlanningLabels:
                if key in PIntersection:
                    single_planning_label = key
                    PlanningCode = Codes.PlanningLabels[single_planning_label]
                    break

    DevelopmentOpportunityDesire = AskForTag("a permitted development opportunity (e.g. Class Q)")
    if DevelopmentOpportunityDesire == "Yes":
        DOIntersection = Codes.DevelopmentOpportunityKeys & LabelSet
        if DOIntersection:
            for key in Codes.DevelopmentOpportunities:
                if key in DOIntersection:
                    single_development_label = key
                    DevelopmentOpportunityCode = Codes.DevelopmentOpportunities[single_development_label]
                    break

    if LPADetails:
        LocalOpportunityDesire = AskForTag("an opportunity in the LPA (e.g. open call for sites)")
        if LocalOpportunityDesire == "Yes":
            CFS = LPADetails.get('cdd1486d583005b9639280aee2bad932857420c7')
            FiveYHLS = LPADetails.get('f2e117864e6d0efef3575ca192321d8ba4f55f28')
            Consequence = LPADetails.get('acb2cab39dcdd362caadd8596fc1870ed0df0da7')
            if CFS == "1002":
                LocalOpportunityCode = "CFS"
            elif FiveYHLS == "991":
                LocalOpportunityCode = "HSNM"
            elif Consequence == "994":
                LocalOpportunityCode = "PSUMP"
            elif Consequence == "995":
                LocalOpportunityCode = "BAP"
            elif Consequence == "1000":
                LocalOpportunityCode = "AP"

    Constraints = DealDetails.get('8bad9f73145375a568e94216e2ae349b96e86333')
    ConstraintsList = Constraints.split(',')
    ConstraintListSet = set(ConstraintsList)

    if TitlePostcodeFormatted:
        PostcodePrefix = TitlePostcodeFormatted[:2] if TitlePostcodeFormatted[1].isalpha() else TitlePostcodeFormatted[:1]
        if PostcodePrefix in LondonPostcodeDistricts:
            LondonOpportunityDesire = AskForTag("a London opportunity (e.g. Opportunity Area)")
            if LondonOpportunityDesire == "Yes":
                LOIntersection = Codes.LondonOpportunityKeys & ConstraintListSet
                if LOIntersection:
                    for key in Codes.LondonOpportunities:
                        if key in LOIntersection:
                            single_london_opportunity = key
                            LondonOpportunityCode = Codes.LondonOpportunities[single_london_opportunity]
                            break

            LondonConstraintDesire = AskForTag("a London constraint")
            if LondonConstraintDesire == "Yes":
                LCIntersection = Codes.LondonConstraintKeys & ConstraintListSet
                if LCIntersection:
                    for key in Codes.LondonConstraints:
                        if key in LCIntersection:
                            single_london_constraint = key
                            LondonConstraintCode = Codes.LondonConstraints[single_london_constraint]
                            break

    GreenConstraintDesire = AskForTag("a green constraint (e.g. Green Belt)")
    if GreenConstraintDesire == "Yes":
        GCIntersection = Codes.GreenConstraintKeys & ConstraintListSet
        if GCIntersection:
            for key in Codes.GreenConstraints:
                if key in GCIntersection:
                    single_green_constraint = key
                    GreenConstraintCode = Codes.GreenConstraints[single_green_constraint]
                    break

    FloodConstraintDesire = AskForTag("a flood constraint (Flood Zone 2/3)")
    if FloodConstraintDesire == "Yes":
        FCIntersection = Codes.FloodConstraintKeys & ConstraintListSet
        if FCIntersection:
            for key in Codes.FloodConstraints:
                if key in FCIntersection:
                    single_flood_constraint = key
                    FloodConstraintCode = Codes.FloodConstraints[single_flood_constraint]
                    break

    HeritageConstraintDesire = AskForTag("a heritage constraint (e.g. Listed Building(s) In Plot)")
    if HeritageConstraintDesire == "Yes":
        HCIntersection = Codes.HeritageConstraintKeys & ConstraintListSet
        if HCIntersection:
            for key in Codes.HeritageConstraints:
                if key in HCIntersection:
                    single_heritage_constraint = key
                    HeritageConstraintCode = Codes.HeritageConstraints[single_heritage_constraint]
                    break

    GeneralConstraintDesire = AskForTag("a general constraint (i.e. mining or coal related)")
    if GeneralConstraintDesire == "Yes":
        GCIntersection = Codes.GeneralConstraintKeys & ConstraintListSet
        if GCIntersection:
            for key in Codes.GeneralConstraints:
                if key in GCIntersection:
                    single_general_constraint = key
                    GeneralConstraintCode = Codes.GeneralConstraints[single_general_constraint]
                    break

    AllCodes = [TemplateCode, LeaseholderCode, PlanningCode, DevelopmentOpportunityCode, LocalOpportunityCode, LondonOpportunityCode, LondonConstraintCode, GreenConstraintCode, FloodConstraintCode, HeritageConstraintCode, GeneralConstraintCode, LandCategoryCode]
    CodeFormatted = '-'.join([Code for Code in AllCodes if Code])
    return CodeFormatted

# Function to generate the letter
def GenerateLetter(CodeFormatted, Salutation):
    AllCodes = CodeFormatted.split('-')
    TemplateCode = AllCodes.pop(0)
    if MailingStatus == "I":
        ChosenTemplate = Templates.Initial[TemplateCode]
    elif MailingStatus == "FU1":
        ChosenTemplate = Templates.FU1[TemplateCode]
    else:
        ChosenTemplate = Templates.FU2[TemplateCode]

    SectionValues = {
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
    for i, section_name in enumerate(PossibleSections):
        if AllCodes:
            NextCode = AllCodes.pop(0)
            NextSection = getattr(Sections, section_name)
            if NextCode in NextSection:
                SectionValues[f'{section_name}Section'] = NextSection[NextCode]

    LPANameFormatted = ''
	Road = ''
	TrainStation = ''
	TrainDistance = ''
	LNTSizeSection = ''
	Substation = ''
	NCA = ''
	
    if LPADetails:
        LPAName = LPADetails.get('name')
        LPANameFormatted = LPAName.replace(" LPA", '')

    SiteName = DealDetails.get('title')
    TitleNumber = DealDetails.get('c78a4fb3140ed97b014b8378291177666df3ff9b')

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
    ChosenTemplate = ChosenTemplate.replace("[PlanningSection]", SectionValues["PlanningSection"])
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
    ChosenTemplate = ChosenTemplate.replace("[LandCategory]", LandCategory.lower())
    ChosenTemplate = ChosenTemplate.replace("[LPANameFormatted]", LPANameFormatted)
    ChosenTemplate = ChosenTemplate.replace("[Email]", Email)
    ChosenTemplate = ChosenTemplate.replace("[Salutation]", Salutation)

    return ChosenTemplate

# Function to run the main process
def run_main_process():
    global DealDetails, LPADetails, TitlePostcodeFormatted, InitialDate, FUDate, MailingStatus, LandCategory, LandCategoryCode, Salutation, Email

    ID = deal_id_entry.get()

    # PD API
    TitlePostcodeFormatted = None
    DealDetailsURL = f"https://api.pipedrive.com/v1/deals/{ID}"
    response = requests.get(DealDetailsURL, params=APIs.PD_query_params)
    if response.status_code == 200:
        DealDetails = response.json().get('data', {})
        TitlePostcode = DealDetails.get('6518beb59dfa14c5c5f38a819924bf7eaee92157')
        if TitlePostcode is not None:
            TitlePostcodeFormatted = TitlePostcode.replace(" ", "")
        else:
            messagebox.showinfo("Information", "Couldn't find any Title Postcode on PipeDrive, so we couldn't gauge metrics such as the closest main road or where the site is exactly.")
    else:
        messagebox.showerror("Error", "Couldn't find this site in PipeDrive.")
        return

    # PD API
    try:
        LPAid = DealDetails.get('824290f62e26f62549d92447ca6fca636c223c2a', {}).get('value')
        LPADetailsURL = f"https://api.pipedrive.com/v1/organizations/{LPAid}"
        response = requests.get(LPADetailsURL, params=APIs.PD_query_params)
        if response.status_code == 200:
            LPADetails = response.json().get('data', {})
        else:
            messagebox.showinfo("Information", "Couldn't find any Linked LPA on PipeDrive, so we couldn't examine any local opportunities.")
    except:
        LPADetails = None
        messagebox.showinfo("Information", "Couldn't find any Linked LPA on PipeDrive, so we couldn't examine any local opportunities.")

    Template = template_var.get()
    TemplateCode = Codes.Templates.get(Template)

    LandCategory = land_category_var.get()
    LandCategoryCode = Codes.LandCategories.get(LandCategory)

    CodeFormatted = GenerateTags(TemplateCode, LandCategoryCode)
    code_text.delete(1.0, tk.END)
    code_text.insert(tk.END, CodeFormatted)

    InitialStatus = initial_status_var.get()
    if InitialStatus == "Yes":
        MailingStatus = "I"
        InitialDate = ''
        FUDate = ''
    else:
        InitialDate = initial_date_entry.get()
        FollowUpStatus = follow_up_status_var.get()
        if FollowUpStatus == '1':
            MailingStatus = "FU1"
            FUDate = ''
        elif FollowUpStatus == '2':
            FUDate = follow_up_date_entry.get()
            MailingStatus = "FU2"

    Association = association_var.get()
    Salutation = Salutations[Association]
    Email = Emails[Association]

    letter = GenerateLetter(CodeFormatted, Salutation)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, letter)

# Initialize the main window
root = tk.Tk()
root.title("Site Tagging Software and Generation")

# Deal ID
deal_id_label = tk.Label(root, text="Enter Deal ID:")
deal_id_label.pack()
deal_id_entry = tk.Entry(root)
deal_id_entry.pack()

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
