from typing import Dict, Any, List
import random

def simple_calculator(hours_per_day: float, days_left: int) -> Dict[str, Any]:
    total_hours = round(hours_per_day * days_left, 2)
    return {'total_hours': total_hours}

def summarizer(texts: List[str], max_chars: int = 400) -> str:
    joined = '\n'.join(texts)
    return joined[:max_chars]

def syllabus_analyzer(syllabus: Dict[str, List[str]]) -> Dict[str, int]:
    counts = {subj: len(topics) for subj, topics in syllabus.items()}
    return counts

def difficulty_adapter(score: float) -> str:
    if score >= 85:
        return 'hard'
    if score >= 60:
        return 'medium'
    return 'easy'

def generate_mcq(subject: str, topic: str, difficulty: str) -> Dict[str, Any]:
    stems = {
        'easy': f'Which statement best describes the basic idea of {topic}?',
        'medium': f'Which of the following is a common application of {topic}?',
        'hard': f'Which advanced property of {topic} is critical for solving complex problems?'
    }
    options = ['Option A', 'Option B', 'Option C', 'Option D']
    answer = random.choice(options)
    return {'type': 'mcq', 'subject': subject, 'topic': topic, 'difficulty': difficulty, 'question': stems[difficulty], 'options': options, 'answer': answer}

def generate_short_question(subject: str, topic: str, difficulty: str) -> Dict[str, Any]:
    q = f'Explain the core concept of {topic} in 2-3 sentences.'
    if difficulty == 'hard':
        q = f'Explain the core concept of {topic} and provide one advanced example.'
    return {'type': 'short', 'subject': subject, 'topic': topic, 'difficulty': difficulty, 'question': q}
