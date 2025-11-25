from typing import Dict, Any, List
from project.tools.tools import generate_mcq, generate_short_question, difficulty_adapter

class Worker:
    def __init__(self, memory: Dict[str, Any] = None):
        self.memory = memory or {}

    def generate_daily_tasks(self, plan: Dict[str, Any], day_index: int = 0) -> Dict[str, Any]:
        if not plan.get('weeks'):
            return {'tasks': [], 'questions': [], 'summary': 'No plan available'}

        week = plan['weeks'][min(day_index // 7, len(plan['weeks'])-1)]
        topics = week.get('topics', [])
        selected = topics[:3]

        tasks = []
        questions = []
        summaries = []

        weak_set = set(self.memory.get('weak_areas', []))
        score = self.memory.get('last_score', 70)
        diff = difficulty_adapter(score)

        for t in selected:
            subj = t['subject']
            topic = t['topic']
            is_weak = t.get('is_weak', topic in weak_set)
            read_time = 30 if not is_weak else 45
            practice_time = 20 if not is_weak else 40
            tasks.append({'type': 'read', 'subject': subj, 'topic': topic, 'duration_mins': read_time})
            tasks.append({'type': 'practice', 'subject': subj, 'topic': topic, 'duration_mins': practice_time})
            questions.append(generate_mcq(subj, topic, diff))
            questions.append(generate_short_question(subj, topic, diff))
            summaries.append(f"{subj} - {topic}: Key points to review and remember.")

        return {'tasks': tasks, 'questions': questions, 'summary': '\n'.join(summaries)}
