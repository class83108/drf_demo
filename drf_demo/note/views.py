from rest_framework import status
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import (
    ListModelMixin,
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
)

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Workspace, Document
from .serializers import (
    WorkspaceSerializer,
    DocumentSerializer,
    WorkspaceDetailSerializer,
)

import json


class WorkspaceDetail(APIView):
    def get_object(self, pk):
        try:
            return Workspace.objects.get(pk=pk)
        except Workspace.DoesNotExist:
            raise Response(status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        workspace = self.get_object(pk)
        serializer = WorkspaceSerializer(workspace)
        return Response(serializer.data)

    def put(self, request, pk):
        workspace = self.get_object(pk)
        serializer = WorkspaceSerializer(workspace, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        workspace = self.get_object(pk)
        workspace.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET", "POST"])
def workspace_list(request):
    if request.method == "GET":
        workspaces = Workspace.objects.all()
        serializer = WorkspaceSerializer(workspaces, many=True)

        return Response(serializer.data)

    elif request.method == "POST":
        serializer = WorkspaceSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def workspace_detail(request, pk):
    try:
        workspace = Workspace.objects.get(pk=pk)
    except Workspace.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = WorkspaceSerializer(workspace)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = WorkspaceSerializer(workspace, data=request.data)

        d_serializer = DocumentSerializer(data=request.data)
        d_serializer.save()
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == "DELETE":
        workspace.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# class WorkspaceList(GenericAPIView):
#     queryset = Workspace.objects.all()
#     serializer_class = WorkspaceSerializer

#     def get(self, request):
#         workspaces = self.get_queryset()
#         serializer = self.get_serializer(workspaces, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = self.get_serializer(data=request.data, many=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WorkspaceDetail(GenericAPIView):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceDetailSerializer

    def get(self, request, pk):
        workspace = self.get_object()
        # serializer = self.get_serializer(workspace, context={"request": request})
        context = self.get_serializer_context()
        context.update({"some_extra_data": "value"})
        serializer = self.get_serializer(workspace, context=context)

        return Response(serializer.data)

    def put(self, request, pk):
        workspace = self.get_object()
        serializer = self.get_serializer(workspace, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        workspace = self.get_object()
        workspace.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WorkspaceList(GenericAPIView, ListModelMixin, CreateModelMixin):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# class WorkspaceDetail(
#     GenericAPIView, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
# ):
#     queryset = Workspace.objects.all()
#     serializer_class = WorkspaceSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)

#     def perform_update(self, serializer):
#         instance = serializer.save()
#         if "members" in self.request.data:
#             instance.members.set(self.request.data["members"])


class WorkspaceList(generics.ListCreateAPIView):
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


# class WorkspaceDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Workspace.objects.all()
#     serializer_class = WorkspaceSerializer

#     def perform_update(self, serializer):
#         instance = serializer.save()
#         if "members" in self.request.data:
#             instance.members.set(self.request.data["members"])


class WorkspaceViewSet(viewsets.ModelViewSet):
    # 限制只允許某些 HTTP 方法
    # http_method_names = ["get"]
    queryset = Workspace.objects.all()
    serializer_class = WorkspaceSerializer

    @action(detail=True, methods=["get"])
    def document_names(self, request, pk=None):
        workspace = self.get_object()
        document_names = workspace.documents.values_list("title", flat=True)
        return Response({"document_names": list(document_names)})
