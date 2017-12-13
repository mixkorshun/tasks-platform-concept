def is_authorized(request):
    return bool(getattr(request, 'user_id'))
