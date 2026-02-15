from unittest import result
from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Max
import json
from .services.llm_service import *
@login_required
def interview_home(request):
    return render(request, 'interviews/interview_home.html')



@login_required
def start_interview(request):

    # ---------------- GET REQUEST ----------------
    if request.method == "GET":
        role = request.GET.get('role')
        difficulty = request.GET.get('difficulty')
        tech_stack = request.GET.get('tech_stack')

        llm_questions = generate_questions(role, difficulty, tech_stack)

        request.session['llm_questions'] = llm_questions
        request.session['role'] = role
        request.session['difficulty'] = difficulty
        request.session['tech_stack'] = tech_stack

        context = {
            "questions": llm_questions,
            "role": role,
            "difficulty": difficulty,
            "tech_stack": tech_stack
        }

        return render(request, "interviews/interviews.html", context)

        # Store selected question IDs in session
        request.session['question_ids'] = [q.id for q in questions]
        request.session['role'] = role
        request.session['difficulty'] = difficulty
        request.session['tech_stack'] = tech_stack

        context = {
            "questions": questions,
            "role": role,
            "difficulty": difficulty,
            "tech_stack": tech_stack
        }

        return render(request, "interviews/interviews.html", context)

# ---------------- POST REQUEST ----------------
    if request.method == "POST":

        questions = request.session.get('llm_questions', [])
        role = request.session.get('role')
        difficulty = request.session.get('difficulty')

        interview_session = InterviewSession.objects.create(
            user=request.user,
            role=role,
            difficulty=difficulty,
            tech_stack=request.session.get('tech_stack')
        )

        qa_data = []

        # STEP 1 → Collect all answers
        for i, question in enumerate(questions):
            user_answer = request.POST.get(f'answer_{i}', "")

            qa_data.append({
                "question": question,
                "answer": user_answer
            })

        # STEP 2 → CALL LLM EVALUATOR 🔥🔥🔥
        llm_results = evaluate_answers(qa_data)

        total_score = 0
        max_score = 0

        # STEP 3 → SAVE ALL FIELDS
        for i, question in enumerate(questions):

            result = llm_results[i] if i < len(llm_results) else {}

            score = result.get("score", 0)
            strengths = "\n".join(result.get("strengths", []))
            weaknesses = "\n".join(result.get("weaknesses", []))
            improvement = result.get("improvement", "")

            total_score += score
            max_score += 100

            Answer.objects.create(
                session=interview_session,
                user_answer=qa_data[i]["answer"],
                score=score,
                strengths=strengths,
                weaknesses=weaknesses,
                improvement=improvement
            )

        # STEP 4 → CALCULATE FINAL %
        percentage = (total_score / max_score) * 100 if max_score > 0 else 0

        interview_session.overall_score = round(percentage, 2)
        interview_session.save()

        # STEP 5 → REDIRECT TO RESULT PAGE
        return redirect("interview_result", session_id=interview_session.id)




@login_required
def interview_history(request):
    sessions = InterviewSession.objects.filter(
        user=request.user
    ).order_by('start_time')

    total_interviews = sessions.count()
    average_score = sessions.aggregate(Avg('overall_score'))['overall_score__avg']
    highest_score = sessions.aggregate(Max('overall_score'))['overall_score__max']

    labels = [f"Interview {i+1}" for i in range(len(sessions))]
    scores = [session.overall_score for session in sessions]

    context = {
        "sessions": sessions,
        "total_interviews": total_interviews,
        "average_score": round(average_score, 2) if average_score else 0,
        "highest_score": highest_score if highest_score else 0,
        "labels_json": json.dumps(labels),
        "scores_json": json.dumps(scores),
    }

    return render(request, "interviews/history.html", context)

@login_required
def result_view(request, session_id):

    interview_session = InterviewSession.objects.get(id=session_id)

    answers = Answer.objects.filter(session=interview_session)

    labels = []
    scores = []
    feedback = []

    for i, ans in enumerate(answers):
        labels.append(f"Q{i+1}")
        scores.append(ans.score)

        feedback.append({
            "score": ans.score,
            "strengths": ans.strengths,
            "weaknesses": ans.weaknesses,
            "improvement": ans.improvement
        })

    context = {
        "session": interview_session,
        "labels_json": json.dumps(labels),
        "scores_json": json.dumps(scores),
        "feedback": feedback
    }

    return render(request, "interviews/result.html", context)
