from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import APIView

from multi_image.serializer import StudentSerializer


class StudentView(APIView):
    def post(self, request):
        serializer = StudentSerializer(
            data=request.data, context={'request': request.FILES})

        if serializer.is_valid():
            serializer.save()
            response = {"status": True, "data": serializer.data}
            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST,
        )
