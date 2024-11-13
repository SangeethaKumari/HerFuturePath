import gradio as gr

# Define individual functions for each tab
def dashboard_tab():
    return "Welcome to the Dashboard! Here, you'll see user progress, recommendations, and milestones."

def learning_pathway_tab():
    return "This is the Learning Pathway page, where you'll find a pathway of learning resources and steps."

# Define a function to list role models
def list_role_models():
    role_models = [
        {"Name": "Dr. Jane Goodall", "Field": "Primatology", "Description": "Known for her groundbreaking research on chimpanzees."},
        {"Name": "Katherine Johnson", "Field": "Mathematics", "Description": "NASA mathematician whose calculations were critical for space missions."},
        {"Name": "Ada Lovelace", "Field": "Computer Science", "Description": "Considered the first computer programmer."},
        {"Name": "Mae Jemison", "Field": "Astronautics", "Description": "First African-American woman in space."},
    ]
    # Format the role models as a list of strings
    formatted_role_models = "\n".join([f"{rm['Name']} - {rm['Field']}: {rm['Description']}" for rm in role_models])
    return formatted_role_models

# Define login/logout functionality
is_logged_in = False  # Initial state for login status

def toggle_login():
    global is_logged_in
    is_logged_in = not is_logged_in
    return "Logout" if is_logged_in else "Login"

# Create Gradio Interface for each tab with a login/logout button
with gr.Blocks() as demo:
    # Row for login/logout button in the top right corner
    with gr.Row():
        gr.Markdown("## HerFuturePath", elem_id="title")
        login_button = gr.Button("Login", elem_id="login_button", visible=True)

    # Tabs section
    with gr.Tabs():
        with gr.Tab("Dashboard"):
            dashboard_output = gr.Textbox(dashboard_tab())
        
        with gr.Tab("Learning Pathway"):
            learning_pathway_output = gr.Textbox(learning_pathway_tab())
        
        with gr.Tab("Role Model Insights"):
            role_model_output = gr.Textbox(list_role_models(), label="Inspiring Role Models")

    # Link login button to the toggle function
    login_button.click(fn=toggle_login, outputs=login_button)

# Launch the app
demo.launch()
