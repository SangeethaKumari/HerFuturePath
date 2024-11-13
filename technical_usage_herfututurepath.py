import gradio as gr

# Define a custom theme class that extends the Soft theme
class CustomSoftTheme(gr.themes.Soft):
    def __init__(self):
        super().__init__()
        # Set custom theme properties here
        super().set(
            body_background_fill="#eef2ff",
            #body_text_color="#6366f1",
            body_text_color="#4f46e5",
            block_background_fill= "#c7d2fe",
            block_label_background_fill="#c7d2fe",
            button_secondary_background_fill="*primary_300",
            button_secondary_text_color = "*primary_500",
            #textbox_background_fill="green"
            )

# Function to display features
def herfuturepath_features():
    features = {
        "BERT Model (bert-base-uncased)": (
            "HerFuturePath uses the BERT model (bert-base-uncased), a pre-trained language model in the BERT family developed by Google, for Masked Language Modeling (MLM). "
            "In MLM, we mask random words in the input sentence, and BERT predicts them based on the context, helping the app understand language patterns in user input."
        ),
        "Zero-Shot Classification": (
            "HerFuturePath leverages zero-shot classification to categorize STEM fields based on users' interests and skills. "
            "The app includes predefined STEM categories like 'Astronomy,' 'Aerospace Engineering,' 'Computer Science,' and 'Data Science.' "
            "Using semantic similarity, zero-shot classification compares user input with these categories, enabling accurate and flexible classification without specific training data for each category."
        ),
        "Skill Gap Analysis": (
            "HerFuturePath performs skill gap analysis using BERT-based word embeddings. "
            "The app converts both user skills and required skills into numerical vectors, capturing the meaning of each skill. "
            "Then, it uses cosine similarity to measure how closely aligned the user’s skills are with those needed in a specific STEM field, identifying gaps where similarity is low. "
            "This process allows HerFuturePath to suggest personalized resources that help users bridge essential skill gaps."
        ),
        "Inspiring Scientist Profiles": (
            "HerFuturePath includes a dataset of inspiring scientists, showcasing their achievements, struggles, and personal stories. "
            "When a user selects a STEM field, the app retrieves relevant scientist profiles and shares their motivational journeys and challenges, providing users with relatable and inspiring examples."
        ),
    }
    return features

# Creating Gradio Interface
def display_features():
    features = herfuturepath_features()
    return "\n\n".join([f"{title}:\n{description}" for title, description in features.items()])

app = gr.Interface(
    fn=display_features,
    inputs=None,
    outputs="text",
    title="HerFuturePath Journey - Technical Features",
    description="An overview of the key technical features in HerFuturePath Journey.",
     allow_flagging="never",
    theme=CustomSoftTheme()
    
)

app.launch()
