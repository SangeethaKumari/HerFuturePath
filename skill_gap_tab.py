import gradio as gr
from transformers import BertTokenizer, BertModel
import torch
import re
import spacy
import requests
from sklearn.metrics.pairwise import cosine_similarity

# Load English tokenizer and tagger
nlp = spacy.load("en_core_web_sm")
# Load pre-trained BERT model and tokenizer
tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")
model = BertModel.from_pretrained("bert-base-uncased")

# Define a set of career-related keywords
career_keywords = ["python", "machine learning", "analytics", "programming", 
                   "algorithms", "java", "cloud", "AI","html"]

default_courses_data = {
    "data science": [
        {"title": "Introduction to Data Science", "instructor": "Dr. Jane Doe", "url": "https://www.udemy.com/data-analysis-basics"},
        {"title": "Machine Learning A-Z", "instructor": "Andrew Ng", "url": "https://www.udemy.com/machine-learning-fundamentals"},
        {"title": "Python for Data Science", "instructor": "DataCamp", "url": "https://www.udemy.com/intro-to-python"}
    ],
    "software": [
        {"title": "Complete Python Bootcamp", "instructor": "Jose Portilla", "url": "https://www.udemy.com/Python"},
        {"title": "Java Programming Masterclass", "instructor": "Tim Buchalka", "url": "https://www.udemy.com/Java"},
        {"title": "Web Development Bootcamp", "instructor": "Colt Steele", "url": "https://www.udemy.com/topic/front-end-web-development"}
    ],
     "general": [
        {"title": "Effective Communication Skills", "instructor": "Alex Morgan", "url": "https://www.udemy.com/Communication"},
        {"title": "Project Management Basics", "instructor": "Sarah Johnson", "url": "https://www.udemy.com/ProductManagement"},
        {"title": "Introduction to Business Analysis", "instructor": "Michael Lee", "url": "https://www.udemy.com/Analysis"}
    ]
}


# Get embeddings for career keywords
career_embeddings = {}
for keyword in career_keywords:
    inputs = tokenizer(keyword, return_tensors="pt")
    outputs = model(**inputs)
    # Use the [CLS] token's embedding
    career_embeddings[keyword] = outputs.last_hidden_state[:, 0, :].detach().numpy()

def get_bert_embedding(word):
    """
    Get the BERT embedding for a single word.
    """
    inputs = tokenizer(word, return_tensors="pt")
    outputs = model(**inputs)
    # Use the [CLS] token's embedding as the representation for the word
    return outputs.last_hidden_state[:, 0, :].detach().numpy()

def extract_career_related_words(words):
    """
    Extract career-related words by comparing each word with career-related keyword embeddings.
    """
    career_related_words = []

    for word in words:
        # Get the embedding for the word
        word_embedding = get_bert_embedding(word)
        
        # Check similarity with each career-related keyword embedding
        for keyword, embedding in career_embeddings.items():
            similarity = cosine_similarity(word_embedding, embedding)[0][0]
            # If similarity is above a threshold, consider the word as career-related
            if similarity > 0.92:  # Threshold can be adjusted
                career_related_words.append(word)
                break  # No need to check other keywords if a match is found

    return set(career_related_words)  # Return unique career-related words

def extract_job_related_keywords(text):
    """
    Extracts job-related related to data science keywords by filtering for nouns and specific job-related terms.
    """
    doc = nlp(text.lower())  # Process text with Spacy
    keywords = {token.text for token in doc if token.pos_ in {"NOUN", "PROPN"}}
    
    # Common job-related terms (expand this list based on your domain)
    job_related_terms = {"python", "java", "project management", "communication","statistical","models", "Algoirthm","numPy","analysis", "aws", "SQL","sql", "cloud", "data", "software", "development", "testing", "api"}
    filtered_keywords = keywords.intersection(job_related_terms)
    return filtered_keywords


def extract_job__keywords(text):
    """
    Extracts job-related related to data science keywords by filtering for nouns and specific job-related terms.
    """
    doc = nlp(text.lower())  # Process text with Spacy
    keywords = {token.text for token in doc if token.pos_ in {"NOUN", "PROPN"}}
    return keywords

def generate_default_courses(missing_skills):
    """
    Dynamically generate default course listings based on missing skills.
    """
    base_url = "https://udemy.com/"
    courses = []

    for skill in missing_skills:
        # Create a title with capitalized words and format the URL
        title = f"{skill.capitalize()} Skills"
        url = f"{base_url}{skill.replace(' ', '')}"
        
        # Add formatted course entry
        courses.append(f"{title} - {url}")

    return courses


def skill_gap(resume_text, job_description_text):
    """
    Compares the resume and job description to identify important job-related keywords that are missing.
    """
    # Extract job-related keywords
    resume_keywords = extract_job__keywords(resume_text)
   
    job_description_keywords = extract_job__keywords(job_description_text)
    job_related_terms = {"python", "java", "project management", "communication","programming","statistical","html","node.js","react","analytics","models", "Algoirthm","numPy", "aws", "SQL","sql", "cloud", "data", "software", "development", "testing", "api"}

    #filtered_keywords = job_description_keywords.intersection(job_related_terms.lower())
    filtered_keywords = extract_career_related_words(job_description_keywords)
    missing_skills = filtered_keywords.intersection(job_related_terms)

    print("job_description_keywords",filtered_keywords)

    if missing_skills:
        result = f"The following job-related skills are missing from the resume: {', '.join(missing_skills)}"
        
        # Get Udemy courses for missing skills
        recommended_courses = get_udemy_courses(missing_skills)
        
        # If no courses are found on Udemy, dynamically generate default courses
        if not recommended_courses:
            recommended_courses = generate_default_courses(missing_skills)
        
        # Format the course list properly with line breaks
        courses_result = "Course link to fill the skill gaps\n\n" + "\n\n".join(recommended_courses)
    else:
        result = "The resume covers all the important job-related skills listed in the job description."
        courses_result = "No additional courses are required."
    return gr.update(value=result, visible=True) ,gr.update(value=courses_result, visible=True)

def get_udemy_courses(missing_skills):
    courses = []
    for skill in missing_skills:
        response = requests.get(
            f"https://www.udemy.com/api-2.0/courses/",
            headers={
                "Authorization": "Basic YOUR_UDEMY_API_KEY",  # Replace with your API key
            },
            params={
                "search": skill,
                "page_size": 2  # Limit to 2 courses per skill for brevity
            },
        )
        if response.status_code == 200:
            course_data = response.json()
            for course in course_data.get("results", []):
                courses.append(f"{course['title']} - {course['url']}")
    return courses

# Function to choose the appropriate default jobs and courses based on subject
def get_default_data(subject, data_dict):
    subject_lower = subject.lower()
    if "data science" in subject_lower:
        return data_dict["data science"]
    elif "software" in subject_lower:
        return data_dict["software"]
    else:
        return data_dict["general"]

