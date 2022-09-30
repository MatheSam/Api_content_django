from .validator import ContentValidator
from rest_framework.views import APIView, Response, Request, status
from django.forms.models import model_to_dict
from .models import Content


class ContentsView(APIView):
    def get(self, request: Request) -> Response:

        contents = Content.objects.all()

        # contents_dict = []
        # for content in contents:
        #     c = model_to_dict(content)
        #     contents_dict.appen(c)

        contents_dict = [model_to_dict(content) for content in contents]

        return Response(contents_dict)

    def post(self, request: Request) -> Response:
        content_verification = ContentValidator(**request.data)

        if not content_verification.is_valid():
            return Response(content_verification.errors, status.HTTP_400_BAD_REQUEST)

        content = Content.objects.create(**request.data)
        content_dict = model_to_dict(content)
        return Response(content_dict, status.HTTP_201_CREATED)


class ContentDetailView(APIView):
    def get(self, request: Request, content_id: int) -> Response:
        try:
            content = Content.objects.get(pk=content_id)
            content_dict = model_to_dict(content)

            return Response(content_dict)

        except Content.DoesNotExist:
            return Response(
                {"message": "Content not found."}, status.HTTP_404_NOT_FOUND
            )

    def patch(self, request: Request, content_id: int) -> Response:
        try:
            content = Content.objects.get(pk=content_id)

            for key, value in request.data.items():
                setattr(content, key, value)

            content.save()
            content_dict = model_to_dict(content)

            return Response(content_dict)

        except Content.DoesNotExist:
            return Response({"error": "Content not found"}, status.HTTP_404_NOT_FOUND)

    def delete(self, request: Request, content_id: int) -> Response:
        try:
            content = Content.objects.get(pk=content_id)
            content.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Content.DoesNotExist:
            return Response({"error": "Content not found"}, status.HTTP_404_NOT_FOUND)


class ContentFindView(APIView):
    def get(self, request: Request) -> Response:
        try:

            # old_query = str(request.query_params)
            # idx = old_query.find(':') + 4
            # new_idx = old_query[idx:].find(':') - 1
            # new_query = old_query[idx:][:new_idx]

            title = request.query_params.get("title", None)

            contents = Content.objects.filter(title__icontains=title)

            contents_dict = [model_to_dict(content) for content in contents]

            if len(contents_dict) == 0:
                raise Content.DoesNotExist

            return Response(contents_dict)

        except Content.DoesNotExist:
            return Response(
                {"error": "Content not found."}, status.HTTP_404_NOT_FOUND
            )
