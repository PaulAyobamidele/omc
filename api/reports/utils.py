# reports/utils.py

from grades.models import GradeEntry

def build_subject_report(student):
    # Fetch grades grouped by subject
    grade_entries = GradeEntry.objects.filter(student=student).select_related(
        "subject", "teacher"
    )

    subjects_map = {}

    for entry in grade_entries:
        sid = entry.subject.id
        if sid not in subjects_map:
            subjects_map[sid] = {
                "subject_id": sid,
                "subject_name": entry.subject.name,
                "teacher_name": f"{entry.teacher.first_name} {entry.teacher.last_name}" if entry.teacher else None,
                "grades": [],
                "total_score": 0,
                "total_maximum": 0,
            }

        subjects_map[sid]["grades"].append({
            "category": entry.category,
            "score": entry.score,
            "maximum": entry.maximum,
            "percentage": round((entry.score / entry.maximum) * 100, 2),
        })

        subjects_map[sid]["total_score"] += entry.score
        subjects_map[sid]["total_maximum"] += entry.maximum

    # compute percentages
    for sid, data in subjects_map.items():
        if data["total_maximum"] > 0:
            data["average_percentage"] = round(
                (data["total_score"] / data["total_maximum"]) * 100, 2
            )
        else:
            data["average_percentage"] = 0.0

    return list(subjects_map.values())
