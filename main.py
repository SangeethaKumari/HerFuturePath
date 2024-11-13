import gradio as gr
from careerpathwayguidance import career_pathway_guidance
from skill_gap_tab import skill_gap
from role_model_tab import list_role_models


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

# Create Gradio Interface with Tabs
with gr.Blocks(theme=CustomSoftTheme(),title="HerFuturePath- Empowering Your Path to Career Success: Real Stories, Real Inspiration ") as demo:

    gr.Markdown("## HerFuturePath", elem_id="title")
    gr.Markdown("Empowering Your Path to Career Success: Real Stories, Real Inspiration")

    # Tabs section
    with gr.Tabs():
          # Tabs section
        with gr.Tab("Home"):
            gr.Markdown("## About HerFuturePath")
            gr.Markdown(
            """
            HerFuturePath goes beyond career exploration focusing on learning and finding inspiration from real-life role models.

            While most career platforms focus solely on skills and job desciptions.
            
            HerFuturePath goes further by providing

                    1. Clear view of key skills, jobs available in the specific career as well as the soft skills required to work on.

                    2. Performs skill gap analysis and recommends courses, projects to build targeted skills.

                    3. Shares real struggles and stories of accomplished women in STEM, showcases their real-life journeys,the challenges they overcame.

            It’s not just about getting a job; it's about seeing yourself in these role models, it’s a journey toward meaningful, motivated careers.

            """
                        )
            #gr.Markdown("## Features")

            #with gr.Row():
                #gr.Markdown("Personalized Career Pathway Guidance")
                #gr.Textbox("Job seekers often don’t have a clear view of the exact skills, roles, or experiences needed to progress in a specific career path.",label="Missing")
                #gr.Textbox("HerFuturePath provides AI-driven, personalized career pathways by giving a clear view of key skills and roles in the specific career.",label="Solution")

            #with gr.Row():
                #gr.Markdown("Skills Gap Analysis")
                #gr.Textbox("Job portals focus on job descriptions rather than providing insights into the skills gaps job seekers may need to fill.",label="Missing")
                #gr.Textbox("HerFuturePath provides the users with the skill gaps and recommends courses, projects to build targeted skills.",label="Solution")

            #with gr.Row():
                #gr.Markdown("Role Models in STEM")
                #gr.Textbox("Job portals often lack visible role models, especially for women in STEM, making it harder for young women to visualize themselves in these careers and feel inspired by relatable success stories",label="Missing")

                #gr.Textbox("HerFuturePath introduces users to female STEM role models from diverse backgrounds.. It showcases real-life journeys , their struggles and stories and the challenges they overcame",label="Solution")
               
        with gr.Tab("Career Pathway Guidance"):
            gr.Markdown("## STEM related jobs")
            gr.Markdown("Enter a STEM-related query to learn about the field.")
            # Inputs and Outputs for Dashboard
            query_input = gr.Textbox(label="Enter your query (e.g., STEM courses in physics)")
            overview_output = gr.Textbox(label="Overview of the career",visible=False)
           
            jobs_output = gr.Textbox(label="Jobs available",visible=False)

            # Button to submit query and fetch data
            submit_button = gr.Button("Submit")

            # Arrange the layout
            submit_button.click(fn=career_pathway_guidance, inputs=query_input,
                                outputs=[overview_output,jobs_output])
                                #outputs=[overview_output, scientist_output, image_output, struggles_output, jobs_output])

        with gr.Tab("Skill Gap Analysis"):
            gr.Markdown("## Job-Related Skill Gap Analysis")
            gr.Markdown("Enter your resume (skills) and job description to identify missing job-related skills.")

            # Input fields for resume and job description
            resume_input = gr.Textbox(label="Resume (Skills)", lines=5, placeholder="Enter your skills here...")
            job_desc_input = gr.Textbox(label="Job Description", lines=5, placeholder="Enter the job description here...")

            # Output fields for skill gaps and recommended courses
            output = gr.Textbox(label="Job-Related Skill Gaps Identified", placeholder="Skill gap analysis will appear here...",visible=False)
            courses_output = gr.Markdown("""  <span style="color: #6366f1;">"Courses to fill the skill gaps"</span> """,visible=False)

            # Submit button to trigger the analysis
            submit_button = gr.Button("Analyze Skill Gaps")
            submit_button.click(skill_gap, inputs=[resume_input, job_desc_input], outputs=[output, courses_output])
        
        with gr.Tab("Role Model Insights"):
            query_input = gr.Textbox(label="Enter your query (e.g., STEM courses in physics)")

             # Output fields for displaying role model information
            scientist_output = gr.Textbox(label="Get inspired by the scientist",visible=False)
            image_output = gr.Image(type="pil", label="Inspiring Scientist",visible=False)
            struggles_output = gr.Textbox(label="Struggles and Successes",visible=False)

            # Button to fetch role model details based on selected field
            fetch_button = gr.Button("Show Role Model")
            fetch_button.click(
                fn=list_role_models, 
                inputs=query_input, 
                outputs=[scientist_output, image_output, struggles_output]
            )

   
# Launch the app
demo.launch()
