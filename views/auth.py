from custom_auth.models import User
from django.core.exceptions import SuspiciousOperation
from django.views.decorators.csrf import csrf_exempt
from ..data import error, error_method_not_allowed, result
from ..helper import get_exception
from ..models import Session
from ..util import authentication_required, json_response


@csrf_exempt
@json_response
def signup(request):
    if request.method == "POST":
        # Receive params
        email = str(request.POST["email"])
        password = str(request.POST["password"])
        # Create object
        obj = User.objects.create_user(email=email, password=password)
        # Prepare response
        data = {
            "email": obj.email,
        }
        return result(data, status=201)
    else:
        return error_method_not_allowed()


@csrf_exempt
@json_response
def signin(request):
    if request.method == "POST":
        # Receive params
        email = str(request.POST["email"])
        password = str(request.POST["password"])
        # Check password
        user = User.objects.get(email=email)
        if not user.check_password(password):
            return error("Invalid password", error_type="check_password", message="Password is invalid", status=400)
        # Create session object
        session = Session.objects.create(user=user)
        # Prepare response
        data = {
            "token": session.token,
        }
        return result(data, status=201)
    else:
        return error_method_not_allowed()