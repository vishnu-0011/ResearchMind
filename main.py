
from dotenv import load_dotenv
load_dotenv()

from graph.builder import build_graph
from agents.base import make_empty_state
from langsmith import Client

def run(topic: str):
    graph  = build_graph()
    state  = make_empty_state(topic)
    result = graph.invoke(state)

    # print findings summary
    print("\n── Sources Used ──")
    for i, source in enumerate(result["sources"]):
        print(f"  [{i+1}] {source}")

    # print critic result
    print(f"\n── Critic Score: {result['score']}/10 ──")
    print(f"Feedback: {result['feedback'][:200]}...")

    # print final report
    print("\n── Final Report ──")
    print(result["final_report"] if result["final_report"] else "!! Report did not pass quality check")


if __name__ == "__main__":
    run("Artificial Intelligence in Healthcare")

    try:
        client = Client()
        client.flush()
        print("\n=> Traces sent to LangSmith")
    except Exception as e:
        print(f"\n=> LangSmith flush (non-critical): {e}")