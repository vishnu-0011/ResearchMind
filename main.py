from dotenv import load_dotenv
load_dotenv()

from graph.builder import build_graph
from agents.base import make_empty_state

def run(topic: str):
    graph = build_graph()
    state = make_empty_state(topic)
    result = graph.invoke(state)
    print("\n── Final Report ──")
    print(result["final_report"])

if __name__ == "__main__":
    run("Artificial Intelligence in Healthcare")