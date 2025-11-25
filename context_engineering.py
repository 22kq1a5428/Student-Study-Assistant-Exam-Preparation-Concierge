from typing import Dict, Any

PLANNER_PROMPT = (
    "You are the strategic study planner. Create an actionable roadmap given the syllabus, exam date, and user profile. "
    "Prioritize weak areas and evenly distribute topics. Return a JSON-like plan with weeks and topic allocations."
)

WORKER_PROMPT = (
    "You are the worker who converts a plan into daily tasks, questions, and summaries. Be concise and actionable. "
    "For each topic provide study tasks and 1-2 questions."
)

EVALUATOR_PROMPT = (
    "You are the evaluator. Validate coverage, feasibility, and difficulty. Return 'APPROVE' or 'REVISION_NEEDED' with reasons."
)

def build_context(agent_name: str, memory: Dict[str, Any]) -> Dict[str, Any]:
    ctx = {'agent': agent_name, 'memory': memory}
    if agent_name == 'planner':
        ctx['prompt'] = PLANNER_PROMPT
    elif agent_name == 'worker':
        ctx['prompt'] = WORKER_PROMPT
    else:
        ctx['prompt'] = EVALUATOR_PROMPT
    return ctx
