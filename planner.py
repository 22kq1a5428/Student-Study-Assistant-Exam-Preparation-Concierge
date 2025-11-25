from typing import Dict, Any, List
from datetime import datetime, timedelta
from project.tools.tools import syllabus_analyzer

class Planner:
    def __init__(self, memory: Dict[str, Any] = None):
        self.memory = memory or {}

    def plan(self, user_profile: Dict[str, Any], syllabus: Dict[str, List[str]], exam_date: str) -> Dict[str, Any]:
        try:
            exam_dt = datetime.fromisoformat(exam_date)
        except Exception:
            exam_dt = datetime.utcnow() + timedelta(days=14)

        today = datetime.utcnow()
        days_left = max((exam_dt - today).days, 1)
        weeks = max(days_left // 7, 1)

        weak = set(self.memory.get('weak_areas', []))
        all_topics = []
        for subj, topics in syllabus.items():
            for t in topics:
                all_topics.append({'subject': subj, 'topic': t, 'is_weak': (t in weak)})

        all_topics.sort(key=lambda x: (not x['is_weak'], x['subject'], x['topic']))

        plan = {'weeks': []}
        topic_idx = 0
        total_topics = len(all_topics)
        base = max(total_topics // weeks, 1)

        for w in range(weeks):
            take = base
            slice_topics = all_topics[topic_idx: topic_idx + take]
            topic_idx += take
            plan['weeks'].append({
                'week': w + 1,
                'start_date': (today + timedelta(days=w*7)).date().isoformat(),
                'end_date': (today + timedelta(days=min((w+1)*7-1, days_left))).date().isoformat(),
                'topics': slice_topics
            })

        if topic_idx < total_topics:
            plan['weeks'].append({
                'week': weeks + 1,
                'start_date': (today + timedelta(days=weeks*7)).date().isoformat(),
                'end_date': exam_dt.date().isoformat(),
                'topics': all_topics[topic_idx:]
            })

        plan['meta'] = {
            'days_left': days_left,
            'total_topics': total_topics,
            'weeks': len(plan['weeks'])
        }
        return plan
