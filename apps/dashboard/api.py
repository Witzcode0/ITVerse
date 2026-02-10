# ListAPI
# 1 - POST - create data
# 2 - GET - get all data
# -------------------------
# DetailAPI
# 3 - GET - get specific data
# 4 - PUT - update specific data with all fields
# {
#     "username":"brijesh",
#     "email": "brijesh@gmail.com",
#     "password": "Admin@123"
# }
# 5 - PATCH - update specific data only
# {
#     "username":"brijesh",
#     "password": "Admin@123"
# }
# 6 - DELETE - delete specific data

# https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from apps.dashboard.models import Contact
from apps.dashboard.serializers import contactSerializers

@api_view(["POST", "GET"])
def contactListAPI(request):
    print("test-1")
    if request.method == "POST":
        print("test-5")
        serializer = contactSerializers(data=request.data)
        if serializer.is_valid():
            print("test-6")
            serializer.save()
            context = {
                "message": "Data created successfully.",
                "status_code": status.HTTP_201_CREATED,
                "data": serializer.data
            }
            print("test-7", context)
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            context = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "errors": serializer.errors
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "GET":
        print("test-2")
        querySet = Contact.objects.all()
        serializer = contactSerializers(querySet, many=True)
        print("test-3")
        context = {
            "message": "All data retive successfully",
            "status_code": status.HTTP_200_OK,
            "data": serializer.data
        }
        print("test-4", context)
        return Response(context, status=status.HTTP_200_OK,)

@api_view(["GET", "PUT", "PATCH", "DELETE"])
def contactDetailAPI(request, contact_id):

    if request.method == "GET":
        pass

    if request.method == "PUT":
        pass

    if request.method == "PATCH":
        pass

    if request.method == "DELETE":
        pass