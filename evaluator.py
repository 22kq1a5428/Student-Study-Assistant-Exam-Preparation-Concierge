from typing import Dict, Any
from project.tools.tools import syllabus_analyzer

class Evaluator:
    def __init__(self, memory: Dict[str, Any] = None):
        self.memory = memory or {}

    def evaluate(self, plan: Dict[str, Any], daily_package: Dict[str, Any]) -> Dict[str, Any]:
        issues = []
        weeks = plan.get('weeks', [])
        if not weeks:
            issues.append('Plan has no weeks/topics')

        tasks = daily_package.get('tasks', [])
        if not tasks:
            issues.append('No daily tasks generated')

        total_mins = sum(t.get('duration_mins', 0) for t in tasks)
        if total_mins > 8 * 60:
            issues.append('Daily workload exceeds 8 hours')

        weak = set(self.memory.get('weak_areas', []))
        scheduled = set()
        for w in weeks[:2]:
            for t in w.get('topics', []):
                scheduled.add(t.get('topic'))

        missing_weak = [w for w in weak if w not in scheduled]
        if missing_weak:
            issues.append(f'Weak topics not scheduled soon: {missing_weak}')

        status = 'APPROVE' if not issues else 'REVISION_NEEDED'
        return {'status': status, 'issues': issues}
