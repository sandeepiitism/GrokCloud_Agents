from phi.agent import Agent
from phi.model.groq import Groq
from dotenv import load_dotenv

# load_dotenv()
GROQ_API_KEY = "gsk_"

agent = Agent(
    model=Groq(id="deepseek-r1-distill-llama-70b", api_key=GROQ_API_KEY)
)



agent.print_response("Share some insights on Indian startups")
