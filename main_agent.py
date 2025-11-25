from project.agents.planner import Planner
from project.agents.worker import Worker
from project.agents.evaluator import Evaluator

class MainAgent:
    def handle_message(self, user_input):
        plan=Planner().plan(user_input)
        work=Worker().work(plan)
        final=Evaluator().evaluate(work)
        return final

def run_agent(user_input:str):
    agent=MainAgent()
    result=agent.handle_message(user_input)
    return result['response']
