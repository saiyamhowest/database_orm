import gradio as gr
import httpx

# Base URL of FastAPI
BASE_URL = "http://127.0.0.1:8000"


conservation_statuses = [
    "Least Concern",
    "Near Threatened",
    "Vulnerable",
    "Endangered",
    "Critically Endangered",
    "Extinct in the Wild",
    "Extinct"
]


# SPECIES FUNCTIONS

# Get all species from API
def get_species():
    data = httpx.get(f"{BASE_URL}/species/").json()
    return [
        [s["id"], s["name"], s["scientific_name"], s["family"],
         s["conservation_status"], s["wingspan_cm"]]
        for s in data
    ]


# Create a new species
def create_species(name, scientific_name, family, status, wingspan):
    if not name or not scientific_name or not family:
        return []

    data = {
        "name": name,
        "scientific_name": scientific_name,
        "family": family,
        "conservation_status": status,
        "wingspan_cm": wingspan
    }

    httpx.post(f"{BASE_URL}/species/", json=data)
    return get_species()

def get_species_choices():
    species = httpx.get(f"{BASE_URL}/species/").json()
    return [(s["name"], s["id"]) for s in species]


# BIRDS FUNCTIONS

# Get all birds
def get_birds():
    data = httpx.get(f"{BASE_URL}/birds/").json()
    return [
        [b["id"], b["nickname"], b["ring_code"], b["age"], b["species_id"]]
        for b in data
    ]


# Create a new bird
def create_bird(nickname, ring_code, age, species_id):
    if not nickname or not ring_code or not species_id:
        return []

    data = {
        "nickname": nickname,
        "ring_code": ring_code,
        "age": int(age),
        "species_id": species_id
    }

    httpx.post(f"{BASE_URL}/birds/", json=data)
    return get_birds()


# Get birds for dropdown
def get_bird_choices():
    birds = httpx.get(f"{BASE_URL}/birds/").json()
    return [(f"{b['nickname']} (#{b['id']})", b["id"]) for b in birds]


# SIGHTINGS FUNCTIONS

# Get all sightings
def get_sightings():
    data = httpx.get(f"{BASE_URL}/birdspotting/").json()
    return [
        [s["id"], s["bird_id"], s["spotted_at"],
         s["location"], s["observer_name"], s.get("notes", "")]
        for s in data
    ]


# Create a new sighting
def create_sighting(bird_id, spotted_at, location, observer_name, notes):
    if not bird_id or not location or not observer_name:
        return []

    data = {
        "bird_id": bird_id,
        "spotted_at": spotted_at,
        "location": location,
        "observer_name": observer_name,
        "notes": notes
    }

    httpx.post(f"{BASE_URL}/birdspotting/", json=data)
    return get_sightings()

# UI

with gr.Blocks() as demo:
    gr.Markdown("#  Bird API Dashboard")

    #Species Section
    gr.Markdown("##  Manage Species")

    species_table = gr.Dataframe(
        headers=["ID", "Name", "Scientific Name", "Family", "Status", "Wingspan"]
    )

    gr.Button("Refresh Species").click(get_species, None, species_table)

    name = gr.Textbox(label="Name")
    scientific_name = gr.Textbox(label="Scientific Name")
    family = gr.Textbox(label="Family")

    conservation_status = gr.Dropdown(
        choices=conservation_statuses,
        label="Conservation Status"
    )

    wingspan = gr.Slider(0, 300, step=5, label="Wingspan")

    gr.Button("Create Species").click(
        create_species,
        [name, scientific_name, family, conservation_status, wingspan],
        species_table
    )

    # Birds Section 
    gr.Markdown("##  Manage Birds")

    birds_table = gr.Dataframe(
        headers=["ID", "Nickname", "Ring Code", "Age", "Species ID"]
    )

    gr.Button("Refresh Birds").click(get_birds, None, birds_table)

    nickname = gr.Textbox(label="Nickname")
    ring_code = gr.Textbox(label="Ring Code")
    age = gr.Number(label="Age")

    b_species = gr.Dropdown(
        choices=get_species_choices(),
        label="Species"
    )

    gr.Button("Create Bird").click(
        create_bird,
        [nickname, ring_code, age, b_species],
        birds_table
    )

    # Sightings Section 
    gr.Markdown("##  Bird Sightings")

    sightings_table = gr.Dataframe(
        headers=["ID", "Bird ID", "Time", "Location", "Observer", "Notes"]
    )

    gr.Button("Refresh Sightings").click(get_sightings, None, sightings_table)

    s_bird = gr.Dropdown(
        choices=get_bird_choices(),
        label="Bird"
    )

    spotted_at = gr.Textbox(label="Time (YYYY-MM-DD HH:MM:SS)")
    location = gr.Textbox(label="Location")
    observer_name = gr.Textbox(label="Observer")
    notes = gr.Textbox(label="Notes")

    gr.Button("Create Sighting").click(
        create_sighting,
        [s_bird, spotted_at, location, observer_name, notes],
        sightings_table
    )


demo.launch()
