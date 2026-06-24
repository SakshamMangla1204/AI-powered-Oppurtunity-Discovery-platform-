from state.research_state import ResearchState


def scoring_agent(state: ResearchState):
    print("\n===== SCORING AGENT =====")

    score = 0

    if state["website"]:
        score += 30

    if state["linkedin"]:
        score += 30

    if state["apply_link"]:
        score += 40

    state["lead_score"] = score

    return state
