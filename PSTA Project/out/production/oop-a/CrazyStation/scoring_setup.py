from resources.helper import *
import re
import json
import pandas as pd

def extract_work_experience(text):
    """
    Extracts the work experience details from the given text and returns a list of dictionaries.
    
    Args:
        text (str): The input text containing the work experience details.
    
    Returns:
        list: A list of dictionaries, where each dictionary represents a work experience.
    """
    work_experiences = []
    lines = text.splitlines()
    
    for i in range(len(lines)):
        if lines[i].startswith("*Von"):
            try:
                work_experience = {}
                work_experience["start_date"] = lines[i].split("*Von")[1].strip()
                work_experience["end_date"] = lines[i+1].split("Enddatum")[1].strip()
                work_experience["company_name"] = lines[i+2].split("*Firmenname")[1].strip()
                work_experience["industry"] = lines[i+3].split("Branche")[1].strip()
                work_experience["job_title"] = lines[i+4].split("*Funktionsbezeichnung")[1].strip()
                work_experience["country"] = lines[i+5].split("Land")[1].strip()
                work_experiences.append(work_experience)
            except IndexError:
                # Skip this work experience if the format is not as expected
                continue
    
    return work_experiences



import re

def extract_language_knowledge(text):
    language_knowledge = []
    pattern = r'\*Sprache(\w+).*?\*Niveau(\w+)'
    matches = re.findall(pattern, text, re.DOTALL)
    
    for match in matches:
        language_name = match[0]
        proficiency_level = match[1]

        # Check if "Englisch" or "Deutsch" is present in the language name
        if "Englisch" in language_name:
            language_name = "Englisch"
        elif "Deutsch" in language_name:
            language_name = "Deutsch"

        language_knowledge.append({"language": language_name, "level": proficiency_level})

    if not language_knowledge:
        print("Language information not found.")

    return language_knowledge

def extract_education_experience(text):
    """
    Extracts the education experience details from the given text and returns a list of dictionaries.
    
    Args:
        text (str): The input text containing the education experience details.
    
    Returns:
        list: A list of dictionaries, where each dictionary represents an education experience.
    """
    education_experiences = []
    lines = text.splitlines()
    index_of_education = []
    end_index = 0
    for i, string in enumerate(lines):
        if "*Von" in string:
            index_of_education.append(i)
    
    if len(index_of_education) != 0:
        if len(index_of_education) == 1:
            bildungseinrightung = False
            education_experience = {}
            for line in lines:
                if "*Von" in line: education_experience["start_date"] = line.replace("*Von","") 
                if "Bis" in line: education_experience["end_date"] = line.replace("Bis","") 
                if "Bildungseinrichtung" in line and bildungseinrightung == False:
                    education_experience["education_type"] = line.replace("Bildungseinrichtung","") 
                    bildungseinrightung = True
                elif "Bildungseinrichtung" in line and bildungseinrightung == True:
                    education_experience["institute_name"] = line.replace("Bildungseinrichtung","") 
                    bildungseinrightung = True
                if "Art des Abschlusses" in line: education_experience["degree"] = line.replace("Art des Abschlusses","") 
                if "Ausbildungsschwerpunkt" in line: education_experience["degree_main_topic"] = line.replace("Ausbildungsschwerpunkt","") 
                if "Abschlussnote" in line: education_experience["final_grade"] = line.replace("Abschlussnote","") 
            education_experiences.append(education_experience)
        else:
            for i in range(len(index_of_education)):
                if i == len(index_of_education) - 1:
                    start_index = index_of_education[i]
                    end_index = len(lines)
                else:
                    start_index = index_of_education[i]
                    end_index = index_of_education[i+1]
                
                bildungseinrightung = False
                education_experience = {}
                for line in lines[start_index:end_index]:
                    if "*Von" in line: education_experience["start_date"] = line.replace("*Von","") 
                    if "Bis" in line: education_experience["end_date"] = line.replace("Bis","") 
                    if "Bildungseinrichtung" in line and bildungseinrightung == False:
                        education_experience["education_type"] = line.replace("Bildungseinrichtung","") 
                        bildungseinrightung = True
                    elif "Bildungseinrichtung" in line and bildungseinrightung == True:
                        education_experience["institute_name"] = line.replace("Bildungseinrichtung","") 
                        bildungseinrightung = True
                    if "Art des Abschlusses" in line: education_experience["degree"] = line.replace("Art des Abschlusses","") 
                    if "Ausbildungsschwerpunkt" in line: education_experience["degree_main_topic"] = line.replace("Ausbildungsschwerpunkt","") 
                    if "Abschlussnote" in line: education_experience["final_grade"] = line.replace("Abschlussnote","") 
                education_experiences.append(education_experience)
    return education_experiences

def get_bmw_file_data(bmw_file):
    if bmw_file:
        candidate_information = {}
        bmw_file_string = read_pdf_contents(f"data/151304/{bmw_file}")
        # print(bmw_file_string)
        candidate_information["Candidate Name"] = bmw_file_string.splitlines()[1]
        candidate_information["Phone"] = bmw_file_string.splitlines()[2].split("\xa0\xa0")[0]
        candidate_information["Email"] = bmw_file_string.splitlines()[2].split("\xa0\xa0")[1]
        for line in bmw_file_string.splitlines():
            if "Land" in line: candidate_information["Country"] = line.replace("Land", "")
            if "angeben" in line: candidate_information["praktikum"] = line.replace("angeben", "")
            if "Eintrittsdatum" in line: candidate_information["eintritts_datum"] = line.replace("Eintrittsdatum", "")
            if "Monaten)" in line: candidate_information["desired_months"] = line.replace("Monaten)", "")
            if "Straßenname" in line: candidate_information["street_name"] = line.replace("Straßenname", "")
            if "Postleitzahl" in line: candidate_information["postleitzahl"] = line.replace("Postleitzahl", "")
            if "Ort" in line: candidate_information["City"] = line.replace("Ort", "")
            if "Geschlecht" in line: candidate_information["Gender"] = line.replace("Geschlecht", "")
        candidate_information["previous_work_experience"] = extract_work_experience(bmw_file_string)
        candidate_information["previous_education"] = extract_education_experience(bmw_file_string.split("Hausnummer")[1])
        candidate_information["languages"] = extract_language_knowledge(bmw_file_string)
        return candidate_information
    else:
        return {}


import datetime

def calculate_work_experience(data):
    """
    Calculates the total number of years of work experience based on the 'previous_work_experience' data in the dictionary.
    If the 'end_date' column has 'TT.MM.JJJJ', it is transformed to the current date.
    
    Args:
        data (dict): The dictionary containing the data.
        
    Returns:
        float: The total number of years of work experience.
    """
    work_experience = data['previous_work_experience']
    total_years = 0.0
    
    for experience in work_experience:
        start_date = datetime.datetime.strptime(experience['start_date'], '%d.%m.%Y')
        
        if experience['end_date'] == 'TT.MM.JJJJ':
            end_date = datetime.datetime.now()
        else:
            end_date = datetime.datetime.strptime(experience['end_date'], '%d.%m.%Y')
        
        duration = end_date - start_date
        years_of_experience = duration.days / 365.25
        total_years += years_of_experience
    
    return round(total_years, 2)
    
def keyword_scoring(subsets_keywords_score, text):
    """
    Calculates the total score of a given text based on the provided subset keyword scores and weights.
    
    Args:
        subsets_keywords_score (dict): A dictionary where the keys are subsets, the values are lists of keywords and their scores, and each subset has a weight.
        text (str): The text to be analyzed.
    
    Returns:
        dict: A dictionary containing the final adjusted scores for each subset.
    """
    subset_scores = {}
    
    # Convert the text to lowercase for case-insensitive matching
    text_lower = text.lower()
    
    for subset, subset_info in subsets_keywords_score.items():
        weight = subset_info["weight"]
        keywords_scores = subset_info["keywords"]
        subset_score = 0
        for keyword_score in keywords_scores:
            keyword = list(keyword_score.keys())[0]
            score = keyword_score[keyword]
            aliases = [keyword.lower()] + [alias.lower() for alias in keyword_score.get("aliases", [])]
            if any(alias in text_lower for alias in aliases):
                subset_score += score
        final_score = subset_score * weight
        subset_scores[subset] = final_score
    
    return subset_scores

def get_column_names(subsets_keywords_score):
    column_names = ['Candidate Name', 'Country', 'City', 'Phone', 'Email', 'Previous Work Experience', 'Previous work related to job?', 'English', 'German']
    for subset in subsets_keywords_score:
        column_names.append(subset)
    return column_names

def generate_candidate_summary(candidate_id: str, subsets_keywords_score: dict):
    bmw_file, candidate_files = get_candidate_application_pdf_data(candidate_id, "data/151304")
    candidate_bmw_data = get_bmw_file_data(bmw_file)
    candidate_content = ""
    for file in candidate_files:
        candidate_content += read_pdf_contents(pdf_file_path=f"data/151304/{file}")
    keyword_scores = keyword_scoring(subsets_keywords_score, candidate_content)
    candidate_bmw_data.update(keyword_scores)
    if candidate_bmw_data["praktikum"] == "":
        candidate_bmw_data["praktikum"] = False
    print(candidate_bmw_data['Candidate Name'])
    candidate_bmw_data['German'] = next((lang['level'] for lang in candidate_bmw_data['languages'] if 'Deutsch' in lang['language']), None)
    candidate_bmw_data['English'] = next((lang['level'] for lang in candidate_bmw_data['languages'] if 'Englisch' in lang['language']), None)
    candidate_bmw_data['Previous Work Experience'] = calculate_work_experience(candidate_bmw_data)
    return candidate_bmw_data


def update_language_proficiency(x):
    #print(x)
    if x:
        if 'Muttersprache' in x:
            return 5
        elif  'Verhandlungssicher' in x :
            return 4
        elif 'Konversationsfähig' in x:
            return 3
        elif 'Grundkenntnisse' in x:
            return 2
        else:
            return 0
    else:
        return 0
def update_column_by_percentiles(df, column_name):
    # Calculate the percentiles for non-zero values
    non_zero_values = df[column_name][df[column_name] > 0]
    p20 = non_zero_values.quantile(0.2)
    p40 = non_zero_values.quantile(0.4)
    p60 = non_zero_values.quantile(0.6)
    p80 = non_zero_values.quantile(0.8)

    # Apply the percentile-based logic
    df[column_name] = df[column_name].apply(lambda x: 0 if x == 0 else (
                                                        1 if x <= p20 else (
                                                            2 if x <= p40 else (
                                                                3 if x <= p60 else (
                                                                    4 if x <= p80 else 5)))))

    return df

def apply_column_transformations(df, subsets_keywords_score):
    # Apply update_language_proficiency to 'English' and 'German' columns
    df['English'] = df['English'].apply(update_language_proficiency)
    df['German'] = df['German'].apply(update_language_proficiency)

    # Remove 'des Wohnsitzes' from 'Country' column
    df['Country'] = df['Country'].str.replace('des Wohnsitzes', '')

    # Apply update_column_by_percentiles to 'Previous Work Experience' column
    df = update_column_by_percentiles(df, 'Previous Work Experience')

    # Apply update_column_by_percentiles to subset columns
    for subset in subsets_keywords_score:
        df = update_column_by_percentiles(df, subset)

    return df

subsets_keywords_score = {
    "Knowledge (Communication Science)": {
        "weight": 5,
        "keywords": [
            {"communication science": 5, "aliases": ["communication studies", "media studies", "journalism", "public relations", "advertising", "Kommunikation", "Kommunikationswissenschaft", "Medientechnik", "Journalismus", "Öffentlichkeitsarbeit", "Werbung"]},
            {"complex topic presentation": 5, "aliases": ["content creation", "information design", "technical writing", "knowledge transfer", "Inhaltserstellung", "iInformationsdesign", "Technisches Schreiben", "Wissensmanagement", "Wissenstransfer"]},
            {"project management skills": 4, "aliases": ["team coordination", "process management", "stakeholder management", "Teamleitung", "Prozessmanagement", "Stakeholdermanagement"]}
        ]
    },
     "Knowledge (Communication)": {
        "weight": 3,
        "keywords": [
            {"communication": 3, "aliases": ["complex topics", "technical writing", "presentation skills", "report writing", "komplexe Themen", "Technisches Schreiben", "Präsentationsfähigkeiten", "Reporting"]},
            {"project management tools": 3, "aliases": ["Confluence", "Jira", "Microsoft Office", "Word", "Excel"]}
        ]
    },
    "Knowledge (Project Management)": {
        "weight": 3,
        "keywords": [
            {"project management": 3, "aliases": ["complex processes", "cross-functional teams", "resource management", "komplexe Prozesse", "crossfunktionale Teams", "Ressourcenmanagement"]},
            {"agile methodologies": 3, "aliases": ["Scrum", "Kanban", "Agile", "Waterfall", "Wasserfall"]}
        ]
    },
    "Knowledge (Automatisation)": {
        "weight": 3,
        "keywords": [
            {"content consolidation": 3, "aliases": ["AI", "Articial intelligence", "KI", "Künstliche Intelligenz", "LLM", "Large Language Model"]},
            {"content creation": 3, "aliases": ["Gen AI", "generative AI", "information clustering", "Text simplification", "Text Vereinfachung"]}
        ]
    },
    "Knowledge (Python)": {
        "weight": 3,
        "keywords": [
            {"Python": 1, "aliases": ["python", "matplotlib", "numpy", "seaborn", "pandas", "django", "flask", "sklearn", "scikit-learn", "scikit learn", "pytorch", "jupyter", "anaconda", "virtualenv"]},
            {"Data Structures": 0.5, "aliases": ["lists", "tuples", "dictionaries", "sets", "arrays"]},
            {"OOP": 0.5, "aliases": ["object-oriented programming", "classes", "inheritance", "polymorphism"]},
            {"Functional Programming": 2, "aliases": ["lambda", "map", "filter", "reduce"]},
            {"Concurrency": 2, "aliases": ["threading", "multiprocessing", "asyncio", "coroutines"]}
        ]
    }
}

df = pd.DataFrame(columns=get_column_names(subsets_keywords_score))

# Iterate through candidate IDs and generate summaries
candidate_ids = list(set([get_application_id(application) for application in get_pdf_files("data/151304")]))
for candidate in candidate_ids:
    try:
        summary = generate_candidate_summary(candidate_id=candidate, subsets_keywords_score=subsets_keywords_score)
        filtered_data = {k: v for k, v in summary.items() if k in df.columns}    
        new_df = pd.DataFrame([filtered_data])
        df = pd.concat([df, new_df], ignore_index=True)
    except:
        print(f"Error processing candidate {candidate}")
        continue

# Apply column transformations
df = apply_column_transformations(df, subsets_keywords_score)

# Export the DataFrame to Excel
df.to_excel('_7_result_application_scoring.xlsx', sheet_name='Sheet', index=False)

