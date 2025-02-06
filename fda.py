import requests
from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv

# load_dotenv()

# Function to query OpenFDA API for adverse events
def query_openfda_adverse_events(drug_name: str, limit: int = 5):
    """Fetches recent adverse events reported for a specific drug from OpenFDA API.
    
    Args:
        drug_name (str): Name of the drug to search for.
        limit (int): Number of results to fetch.
    
    Returns:
        list: List of dictionaries containing relevant event data.
    """
    base_url = "https://api.fda.gov/drug/event.json"
    query = f"search=patient.drug.medicinalproduct:{drug_name}&limit={limit}"
    url = f"{base_url}?{query}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        if "results" in data:
            return data["results"]
        else:
            return [{"error": "No results found."}]
    else:
        return [{"error": f"Failed to fetch data: {response.status_code}"}]

# OpenFDA API Key (if required, though OpenFDA does not mandate it)
GROQ_API_KEY = "gsk_"

# Define agent
agent = Agent(
    model=Groq(id="deepseek-r1-distill-llama-70b", api_key=GROQ_API_KEY),
    tools=[query_openfda_adverse_events],
    instructions=[
        "Use tables to display OpenFDA data.",
        "Ensure returned data is formatted properly before passing it to the response handler.",
    ],
    show_tool_calls=True,
    markdown=True,
    debug_mode=True,
)

# Example query: Get recent adverse events for Ibuprofen
response_data = query_openfda_adverse_events("Ibuprofen", limit=10)
if isinstance(response_data, list):
    for entry in response_data:
        print(entry)  # Debugging: Print each entry to verify data format

agent.print_response(
    f"Retrieved {len(response_data)} adverse events for Ibuprofen from OpenFDA.",
    stream=True
)
