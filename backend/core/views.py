from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response


@api_view(["GET"])
@permission_classes([AllowAny])
def health(request):
    data = {
        "status": "ok",
        "service": "abiturend-backend",
        "version": "1.0",
    }
    return Response(data)


# Living endpoint catalogue. `core.tests` asserts every entry still resolves,
# so the docs cannot silently rot out of sync with the router.
API_VERSION = "1.0"

API_ENDPOINTS = [
    {
        "path": "/api/",
        "method": "GET",
        "auth": "public",
        "purpose": "This index: discover every endpoint of the platform.",
    },
    {
        "path": "/api/health/",
        "method": "GET",
        "auth": "public",
        "purpose": "Service health probe for load balancers and monitoring.",
    },
    {
        "path": "/api/auth/csrf/",
        "method": "GET",
        "auth": "public",
        "purpose": "CSRF token for session-authenticated requests.",
    },
    {
        "path": "/api/auth/register/",
        "method": "POST",
        "auth": "public",
        "purpose": "Create a student account.",
    },
    {
        "path": "/api/auth/login/",
        "method": "POST",
        "auth": "public",
        "purpose": "Authenticate with a session cookie.",
    },
    {
        "path": "/api/auth/logout/",
        "method": "POST",
        "auth": "session",
        "purpose": "Destroy the active session.",
    },
    {
        "path": "/api/auth/me/",
        "method": "GET, PATCH",
        "auth": "session",
        "purpose": "Read or update the current user's profile.",
    },
    {
        "path": "/api/auth/change-password/",
        "method": "POST",
        "auth": "session",
        "purpose": "Update the current user's password.",
    },
    {
        "path": "/api/subjects/",
        "method": "GET",
        "auth": "public",
        "purpose": "List subjects (question counts included).",
    },
    {
        "path": "/api/subjects/{slug}/",
        "method": "GET",
        "auth": "public",
        "purpose": "A single subject; nested topics are embedded.",
    },
    {
        "path": "/api/topics/",
        "method": "GET",
        "auth": "public",
        "purpose": "List topics.",
    },
    {
        "path": "/api/topics/{id}/",
        "method": "GET",
        "auth": "public",
        "purpose": "Topic detail; nested subtopics embedded.",
    },
    {
        "path": "/api/questions/",
        "method": "GET, POST",
        "auth": "GET any authenticated, POST teacher/admin",
        "purpose": "Browse (students see only published; is_correct hidden) or manage the bank.",
    },
    {
        "path": "/api/questions/{id}/",
        "method": "GET, PUT, PATCH, DELETE",
        "auth": "write teacher/admin, GET student",
        "purpose": "Question detail; students never receive correct-answer flags.",
    },
    {
        "path": "/api/sessions/",
        "method": "GET, POST",
        "auth": "session",
        "purpose": "Create a practice/exam session from a random question pool, or list own sessions.",
    },
    {
        "path": "/api/sessions/{id}/",
        "method": "GET",
        "auth": "session",
        "purpose": "Session summary (status, progress, score so far).",
    },
    {
        "path": "/api/sessions/{id}/current/",
        "method": "GET",
        "auth": "session",
        "purpose": "Next unanswered question.",
    },
    {
        "path": "/api/sessions/{id}/questions/",
        "method": "GET",
        "auth": "session",
        "purpose": "All session questions (correct answers hidden) for exam navigation.",
    },
    {
        "path": "/api/sessions/{id}/answer/",
        "method": "POST",
        "auth": "session",
        "purpose": "Submit an answer; returns immediate feedback (correctness, explanation).",
    },
    {
        "path": "/api/sessions/{id}/finish/",
        "method": "POST",
        "auth": "session",
        "purpose": "Finish the session and receive the full score report.",
    },
    {
        "path": "/api/sessions/{id}/report/",
        "method": "GET",
        "auth": "session",
        "purpose": "Read-only question-by-question review for a session.",
    },
    {
        "path": "/api/universities/",
        "method": "GET",
        "auth": "public",
        "purpose": "University catalogue with available directions and entrance subjects.",
    },
    {
        "path": "/api/universities/{slug}/",
        "method": "GET",
        "auth": "public",
        "purpose": "A single university; nested directions embedded.",
    },
    {
        "path": "/api/directions/",
        "method": "GET",
        "auth": "public",
        "purpose": "Directions filterable by university slug or admission subject.",
    },
    {
        "path": "/api/stats/summary/",
        "method": "GET",
        "auth": "session",
        "purpose": "Aggregated learner analytics: accuracy, streak, weekly activity, subject breakdown, weak topics, recent sessions.",
    },
]


@api_view(["GET"])
@permission_classes([AllowAny])
def api_root(request):
    data = {
        "title": "Abiturend Platform API",
        "version": API_VERSION,
        "endpoints": API_ENDPOINTS,
    }
    return Response(data)