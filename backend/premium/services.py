from django.utils import timezone

from .models import Subscription

FREE_TIER_DAILY_LIMIT = 3


def active_subscription(user):
    """The most recent active subscription for ``user``, or None."""
    if not user or not user.is_authenticated:
        return None
    return (
        Subscription.objects.filter(user=user, ends_at__gt=timezone.now())
        .select_related("plan")
        .order_by("-created_at")
        .first()
    )


def is_premium(user):
    return active_subscription(user) is not None


def daily_session_limit(user):
    """Sessions a user may start per day; None means unlimited."""
    sub = active_subscription(user)
    if sub is not None:
        limit = sub.plan.max_sessions_per_day
        if limit is None:
            return None
        # A paying plan that still carries a cap is honored as-is.
        return limit
    return FREE_TIER_DAILY_LIMIT


def sessions_started_today(user):
    today = timezone.localdate()
    from practice.models import PracticeSession

    return PracticeSession.objects.filter(
        user=user, started_at__date=today
    ).count()


def remaining_sessions_today(user):
    """How many more sessions the user may start today. None = unlimited."""
    limit = daily_session_limit(user)
    if limit is None:
        return None
    return max(0, limit - sessions_started_today(user))


def can_start_session(user):
    remaining = remaining_sessions_today(user)
    if remaining is None:
        return True, None
    return remaining > 0, remaining