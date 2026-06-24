from langgraph.graph import END, StateGraph

from state.research_state import ResearchState

from agents.research import research_agent
from agents.contact import contact_agent

builder = StateGraph(ResearchState)

builder.add_node("research", research_agent)
builder.add_node("contact", contact_agent)

builder.set_entry_point("research")

builder.add_edge("research", "contact")
builder.add_edge("contact", END)

graph = builder.compile()
