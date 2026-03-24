import gradio as gr
import httpx

# API base URL
BASE_URL = "http://127.0.0.1:8000"

# Conservation status list
conservation_statuses = [
    "Least Concern",
    "Near Threatened",
    "Vulnerable",
    "Endangered",
    "Critically Endangered",
    "Extinct in the Wild",
    "Extinct"
]

# Get all species
def get_species():
    try:
        data = httpx.get(f"{BASE_URL}/species/").json()
        return [[s["id"], s["name"], s["scientific_name"], s["family"],
                 s["conservation_status"], s["wingspan_cm"]] for s in data]
    except:
        return []

# Create a species
def create_species(name, scientific_name, family, status, wingspan):
    if not name or not scientific_name or not family:
        return get_species(), "Please fill all fields"

    try:
        httpx.post(f"{BASE_URL}/species/", json={
            "name": name,
            "scientific_name": scientific_name,
            "family": family,
            "conservation_status": status,
            "wingspan_cm": wingspan
        })
        return get_species(), "Species created"
    except:
        return get_species(), "Error creating species"

# Get species for dropdown
def get_species_choices():
    try:
        species = httpx.get(f"{BASE_URL}/species/").json()
        return [(s["name"], s["id"]) for s in species]
    except:
        return []

# Filter species by status
def filter_species(status):
    data = httpx.get(f"{BASE_URL}/species/").json()
    return [[s["id"], s["name"], s["scientific_name"], s["family"],
             s["conservation_status"], s["wingspan_cm"]]
            for s in data if s["conservation_status"] == status]

# Get all birds
def get_birds():
    try:
        data = httpx.get(f"{BASE_URL}/birds/").json()
        return [[b["id"], b["nickname"], b["ring_code"],
                 b["age"], b["species_id"]] for b in data]
    except:
        return []

# Create a bird
def create_bird(nickname, ring_code, age, species_id):
    if not nickname or not ring_code or not species_id:
        return get_birds(), "Please fill all fields"

    try:
        httpx.post(f"{BASE_URL}/birds/", json={
            "nickname": nickname,
            "ring_code": ring_code,
            "age": int(age),
            "species_id": species_id
        })
        return get_birds(), "Bird created"
    except:
        return get_birds(), "Error creating bird"

# Get birds for dropdown
def get_bird_choices():
    try:
        birds = httpx.get(f"{BASE_URL}/birds/").json()
        return [(f"{b['nickname']} (#{b['id']})", b["id"]) for b in birds]
    except:
        return []

# Get all sightings
def get_sightings():
    try:
        data = httpx.get(f"{BASE_URL}/birdspotting/").json()
        return [[s["id"], s["bird_id"], s["spotted_at"],
                 s["location"], s["observer_name"], s.get("notes", "")]
                for s in data]
    except:
        return []

# Create a sighting
def create_sighting(bird_id, time, location, observer, notes):
    if not bird_id or not location or not observer:
        return get_sightings(), "Please fill all fields"

    try:
        httpx.post(f"{BASE_URL}/birdspotting/", json={
            "bird_id": bird_id,
            "spotted_at": time,
            "location": location,
            "observer_name": observer,
            "notes": notes
        })
        return get_sightings(), "Sighting created"
    except:
        return get_sightings(), "Error creating sighting"

# UI
with gr.Blocks() as demo:
    gr.Markdown("# Bird API Dashboard")

    gr.Markdown("## Species")

    species_table = gr.Dataframe(
        headers=["ID", "Name", "Scientific", "Family", "Status", "Wingspan"]
    )

    species_msg = gr.Markdown()

    gr.Button("Refresh").click(get_species, None, species_table)

    filter_dd = gr.Dropdown(conservation_statuses, label="Filter")
    gr.Button("Apply Filter").click(filter_species, filter_dd, species_table)

    name = gr.Textbox(label="Name")
    sci = gr.Textbox(label="Scientific Name")
    fam = gr.Textbox(label="Family")
    status = gr.Dropdown(conservation_statuses, label="Status")
    wing = gr.Slider(0, 300, step=5, label="Wingspan")

    gr.Button("Create Species").click(
        create_species,
        [name, sci, fam, status, wing],
        [species_table, species_msg]
    )

    gr.Markdown("## Birds")

    birds_table = gr.Dataframe(
        headers=["ID", "Nickname", "Ring", "Age", "Species"]
    )

    bird_msg = gr.Markdown()

    gr.Button("Refresh").click(get_birds, None, birds_table)

    nickname = gr.Textbox(label="Nickname")
    ring = gr.Textbox(label="Ring Code")
    age = gr.Number(label="Age")

    species_dd = gr.Dropdown(get_species_choices(), label="Species")

    gr.Button("Refresh Species List").click(
        get_species_choices, None, species_dd
    )

    gr.Button("Create Bird").click(
        create_bird,
        [nickname, ring, age, species_dd],
        [birds_table, bird_msg]
    )

    gr.Markdown("## Sightings")

    sight_table = gr.Dataframe(
        headers=["ID", "Bird", "Time", "Location", "Observer", "Notes"]
    )

    sight_msg = gr.Markdown()

    gr.Button("Refresh").click(get_sightings, None, sight_table)

    bird_dd = gr.Dropdown(get_bird_choices(), label="Bird")
    time = gr.Textbox(label="Time")
    loc = gr.Textbox(label="Location")
    obs = gr.Textbox(label="Observer")
    notes = gr.Textbox(label="Notes")

    gr.Button("Refresh Bird List").click(
        get_bird_choices, None, bird_dd
    )

    gr.Button("Create Sighting").click(
        create_sighting,
        [bird_dd, time, loc, obs, notes],
        [sight_table, sight_msg]
    )

demo.launch()