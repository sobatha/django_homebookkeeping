from django.utils import timezone

def common(request):
    now = timezone.now()

    return {"now_year": now.year,
            "now_month": now.month}