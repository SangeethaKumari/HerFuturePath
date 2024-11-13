import gradio as gr
from PIL import Image
from io import BytesIO
import requests


# Sample dataset of inspiring scientists with associated subjects, real image URLs, and struggles
scientist_dataset = {
    "physics": {
        "name": "Marie Curie",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/9/92/Marie_Curie_c._1920s_%28cropped%29.jpg",
        "info": "Marie Curie pioneered research on radioactivity and was the first person to win Nobel Prizes in both Physics and Chemistry.",
        "struggles_and_success": "Curie faced financial hardship, gender discrimination, and health risks due to exposure to radioactive materials. Despite these challenges, she became a foundational figure in modern physics.",
        "jobs_available": ["Research Physicist", "Nuclear Physicist", "Medical Physicist", "Physics Professor", "Data Scientist"]
    },
    "chemistry": {
        "name": "Dorothy Hodgkin",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/a/a0/Dorothy_Hodgkin_%281960%29.jpg",
        "info": "Dorothy Hodgkin was awarded the Nobel Prize in Chemistry for her work in X-ray crystallography.",
        "struggles_and_success": "Hodgkin faced limited research funding and gender bias throughout her career. Her work in biochemistry revolutionized medicine.",
        "jobs_available": ["Analytical Chemist", "Biochemist", "Pharmaceutical Chemist", "Research Scientist", "Lab Technician"]
    },
    "biology": {
        "name": "Rosalind Franklin",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/f/fd/Rosalind_Franklin_%28retouched%29.jpg",
        "info": "Rosalind Franklin’s work on X-ray diffraction was crucial to discovering the double helix structure of DNA.",
        "struggles_and_success": "Franklin faced gender discrimination and was not fully credited for her contributions to the discovery of DNA structure during her lifetime.",
        "jobs_available": ["Geneticist", "Molecular Biologist", "Microbiologist", "Biotechnologist", "Biology Professor"]
    },
    "mathematics": {
        "name": "Ada Lovelace",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/a/a4/Ada_Lovelace_portrait.jpg",
        "info": "Ada Lovelace is regarded as the first computer programmer due to her work on Charles Babbage's Analytical Engine.",
        "struggles_and_success": "Lovelace’s ideas were not fully recognized until the modern computer age, and she pursued her work despite societal expectations limiting women's roles.",
        "jobs_available": ["Data Analyst", "Cryptographer", "Mathematics Professor", "Data Scientist", "Operations Research Analyst"]
    },
    "engineering": {
        "name": "Grace Hopper",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/a/ad/Commodore_Grace_M._Hopper%2C_USN_%28covered%29.jpg",
        "info": "Grace Hopper was a pioneer in computer programming, creating one of the first compilers and contributing to the COBOL language.",
        "struggles_and_success": "Hopper faced gender discrimination in a male-dominated field and was initially rejected from the Navy due to age and weight restrictions.",
        "jobs_available": ["Software Engineer", "Systems Engineer", "Mechanical Engineer", "Electrical Engineer", "Civil Engineer"]
    },
    "electronics": {
        "name": "Hedy Lamarr",
        "image_url": "https://en.wikipedia.org/wiki/File:Hedy_Lamarr_Publicity_Photo_for_The_Heavenly_Body_1944.jpg",
        "info": "Hedy Lamarr co-invented a frequency-hopping technology, which later became foundational for modern wireless communication.",
        "struggles_and_success": "Despite her invention, Lamarr faced dismissal due to her acting career overshadowing her scientific contributions. Her work was only recognized posthumously.",
        "jobs_available": ["Electronics Engineer", "RF Engineer", "Telecommunications Engineer", "Embedded Systems Engineer", "Signal Processing Engineer"]
    },
    "electrical": {
        "name": "Edith Clarke",
        "image_url": "https://upload.wikimedia.org/wikipedia/en/9/92/Edith_Clarke.jpg",
        "info": "Edith Clarke was the first female electrical engineer and the first woman to deliver a paper at the American Institute of Electrical Engineers.",
        "struggles_and_success": "Clarke faced gender barriers and a lack of employment opportunities for women, but her persistence led her to make important contributions to electrical engineering.",
        "jobs_available": ["Electrical Engineer", "Power Systems Engineer", "Controls Engineer", "Electrical Technician", "Automation Engineer"]
    },
    "chemical": {
        "name": "Alice Ball",
        "image_url": "https://en.wikipedia.org/wiki/File:Alice_Augusta_Ball.jpg",
        "info": "Alice Ball developed the first effective treatment for leprosy, known as the 'Ball Method,' in the early 1900s.",
        "struggles_and_success": "Ball faced racial and gender discrimination throughout her education and career. Her work was initially uncredited but later recognized for its impact in medicine.",
        "jobs_available": ["Chemical Engineer", "Process Engineer", "Materials Scientist", "Petroleum Engineer", "Pharmaceutical Engineer"]
    },
    "software": {
        "name": "Margaret Hamilton",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/6/68/Margaret_Hamilton_1995.jpg",
        "info": "Margaret Hamilton was a software engineer whose work on the Apollo mission's flight software was crucial to landing humans on the moon.",
        "struggles_and_success": "Hamilton faced a lack of respect for software engineering as a legitimate discipline. Her pioneering work in software reliability laid the foundation for modern software engineering.",
        "jobs_available": ["Software Developer", "Front-End Developer", "Back-End Developer", "Full Stack Developer", "DevOps Engineer"]
    },
    "environment": {
        "name": "Rachel Carson",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/f/f4/Rachel-Carson.jpg",
        "info": "Rachel Carson was an environmental scientist and author whose work 'Silent Spring' helped launch the environmental movement.",
        "struggles_and_success": "Carson faced criticism and opposition from the chemical industry for exposing the dangers of pesticides, yet her work led to significant environmental regulations.",
        "jobs_available": ["Environmental Scientist", "Ecologist", "Environmental Consultant", "Conservation Scientist", "Environmental Engineer"]
    },
    "finance": {
        "name": "Muriel Siebert",
        "image_url": "https://en.wikipedia.org/wiki/File:60s_Muriel_Siebert_advertisement_(cropped).jpg",
        "info": "Muriel Siebert was the first woman to own a seat on the New York Stock Exchange and founded one of the first discount brokerage firms.",
        "struggles_and_success": "Siebert faced significant gender discrimination on Wall Street but became a pioneer in finance, advocating for women’s rights and financial education.",
        "jobs_available": ["Financial Analyst", "Investment Banker", "Risk Manager", "Portfolio Manager", "Financial Consultant"]
    },
    "data science": {
        "name": "Fei-Fei Li",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/c/c7/Fei-Fei_Li_at_AI_for_Good_2017.jpg",
        "info": "Fei-Fei Li is a pioneering computer scientist known for her work in computer vision and AI, particularly with the ImageNet project.",
        "struggles_and_success": "Fei-Fei Li faced cultural and gender barriers as an immigrant in the U.S. Despite being one of the few women in a male-dominated field, Dr. Li’s resilience and passion for ethical AI and diversity have driven her to advocate for women in STEM and inspire the next generation.",
        "jobs_available": ["Data Scientist", "Machine Learning Engineer", "Data Analyst", "AI Research Scientist", "Business Intelligence Analyst"]
    }
}


# Function to fetch an image and struggles for a subject
def fetch_scientist_image_and_struggles(subject):
    if subject in scientist_dataset:
        scientist_info = scientist_dataset[subject]
        image_url = scientist_info["image_url"]
        scientist_name = scientist_info["name"]
        
        try:
            response = requests.get(image_url, stream=True)
            response.raise_for_status()
            if "image" in response.headers["Content-Type"]:
                image = Image.open(BytesIO(response.content)).resize((256, 256), Image.LANCZOS)
            else:
                image = Image.new('RGB', (256, 256), color='grey')
        except Exception as e:
            print(f"Error fetching image: {e}")
            image = Image.new('RGB', (256, 256), color='grey')

        struggles_and_success = scientist_info["struggles_and_success"]
        return scientist_name, image, struggles_and_success
    else:
        return None, Image.new('RGB', (256, 256), color='grey'), "No information available."

# Main function to handle user query
def list_role_models(query):
    scientist_name, image, struggles_and_success = fetch_scientist_image_and_struggles(query)
    return gr.update(value=scientist_name, visible=True),gr.update(value=image, visible=True),gr.update(value=struggles_and_success, visible=True)
    #return  scientist_name, image, struggles_and_success




