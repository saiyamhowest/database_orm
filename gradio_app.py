import gradio as gr
import httpx

BASE_URL = "http://127.0.0.1:8000"

# API FUNCTIONS

def get_species():
    response = httpx.get(f"{BASE_URL}/species/")
    return response.json()


def create_species(name, scientific_name, family, status, wingspan):
    data = {
        "name": name,
        "scientific_name": scientific_name,
        "family": family,
        "conservation_status": status,
        "wingspan_cm": wingspan
    }

    response = httpx.post(f"{BASE_URL}/species/", json=data)
    return get_species()  # refresh table after insert

# UI

with gr.Blocks() as demo:
    gr.Markdown("# 🐦 Bird API Dashboard")
    gr.Markdown("### Manage Species")

    # TABLE
    species_table = gr.Dataframe()

    refresh_btn = gr.Button("🔄 Refresh Species")

    # FORM
    gr.Markdown("### ➕ Add New Species")

    name = gr.Textbox(label="Name")
    scientific_name = gr.Textbox(label="Scientific Name")
    family = gr.Textbox(label="Family")

    conservation_status = gr.Dropdown(
        choices=[
            "Least Concern",
            "Near Threatened",
            "Vulnerable",
            "Endangered",
            "Critically Endangered"
        ],
        label="Conservation Status"
    )

    wingspan = gr.Slider(0, 300, step=5, label="Wingspan (cm)")

    create_btn = gr.Button("Create Species")

    # EVENTS

    refresh_btn.click(
        fn=get_species,
        inputs=[],
        outputs=species_table
    )

    create_btn.click(
        fn=create_species,
        inputs=[name, scientific_name, family, conservation_status, wingspan],
        outputs=species_table
    )

# RUN

demo.launch()