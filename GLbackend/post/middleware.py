from account.models import UserVisit
from datetime import date


class UserVisitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        # Get the path of the visited page
        visited_path = request.path

        current_date = date.today()

        if visited_path == "/api/posts/discussion_posts":
            # Log the user visit to the discussion page in your database
            if not UserVisit.objects.filter(
                user=request.user,
                visited_page=visited_path,
                visit_datetime__date=current_date,
            ).exists():
                UserVisit.objects.create(user=request.user, visited_page=visited_path)
        if visited_path == "/api/posts/marketplace_posts/":
            if not UserVisit.objects.filter(
                user=request.user,
                visited_page=visited_path,
                visit_datetime__date=current_date,
            ).exists():
                UserVisit.objects.create(user=request.user, visited_page=visited_path)

        if visited_path == "/api/posts/connect_posts/":
            if not UserVisit.objects.filter(
                user=request.user,
                visited_page=visited_path,
                visit_datetime__date=current_date,
            ).exists():
                UserVisit.objects.create(user=request.user, visited_page=visited_path)

        if visited_path == "/api/posts/tournament_posts/":
            if not UserVisit.objects.filter(
                user=request.user,
                visited_page=visited_path,
                visit_datetime__date=current_date,
            ).exists():
                UserVisit.objects.create(user=request.user, visited_page=visited_path)

        if visited_path == "/api/posts/beta_posts/":
            if not UserVisit.objects.filter(
                user=request.user,
                visited_page=visited_path,
                visit_datetime__date=current_date,
            ).exists():
                UserVisit.objects.create(user=request.user, visited_page=visited_path)

        return response
