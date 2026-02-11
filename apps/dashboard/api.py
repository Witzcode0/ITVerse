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

    if request.method == "GET":
        querySet = Contact.objects.all()
        serializer = contactSerializers(querySet, many=True)
        context = {
            "message": "All data retive successfully",
            "status_code": status.HTTP_200_OK,
            "data": serializer.data
        }
        return Response(context, status=status.HTTP_200_OK)
    
    if request.method == "POST":
        print(request.data['email'], "-----")
        serializer = contactSerializers(data=request.data)
        if serializer.is_valid():
            serializer.save()
            context = {
                "message": "Data created successfully.",
                "status_code": status.HTTP_201_CREATED,
                "data": serializer.data
            }
            return Response(context, status=status.HTTP_201_CREATED)
        else:
            context = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "errors": serializer.errors
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

@api_view(["GET", "PUT", "PATCH", "DELETE"])
def contactDetailAPI(request, contact_id):

    try:
        querySet = Contact.objects.get(id=contact_id)
    except Contact.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = contactSerializers(querySet)
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "PUT":
        serializer = contactSerializers(querySet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            context = {
                "message": "Data updated successfully.",
                "status_code": status.HTTP_200_OK,
                "data": serializer.data
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            context = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "errors": serializer.errors
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "PATCH":
        serializer = contactSerializers(querySet, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            context = {
                "message": "Data updated successfully.",
                "status_code": status.HTTP_200_OK,
                "data": serializer.data
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            context = {
                "status_code": status.HTTP_400_BAD_REQUEST,
                "errors": serializer.errors
            }
            return Response(context, status=status.HTTP_400_BAD_REQUEST)

    if request.method == "DELETE":
        querySet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)