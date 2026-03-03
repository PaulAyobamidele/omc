from django.http import JsonResponse
from .models import School


class TenantMiddleware:
    """
    Reads X-School-Slug header and attaches the School instance to the request.
    Skips resolution for paths that don't need a school context
    (admin panel, school registration, schema endpoints).
    """
    EXEMPT_PATHS = (
        '/admin/',
        '/api/schools/register/',
        '/api/schema/',
        '/swagger/',
    )

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.school = None

        path = request.path_info
        if any(path.startswith(p) for p in self.EXEMPT_PATHS):
            return self.get_response(request)

        slug = request.headers.get('X-School-Slug')
        if slug:
            try:
                school = School.objects.get(slug=slug, is_active=True)
                request.school = school
            except School.DoesNotExist:
                return JsonResponse(
                    {'detail': f'School "{slug}" not found or inactive.'},
                    status=404,
                )

        return self.get_response(request)
