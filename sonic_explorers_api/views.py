from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view()
def root_route(request):
    return Response(
        {
            "message": "Welcome to the Sonic Explorers API. "
            "For more information please refer to the documentation at "
            "https://github.com/nacht-falter/sonic-explorers-api"
        }
    )
