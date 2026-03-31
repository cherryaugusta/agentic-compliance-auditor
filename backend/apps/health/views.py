import redis
from django.conf import settings
from django.db import connection
from rest_framework.response import Response
from rest_framework.views import APIView


class LiveView(APIView):
    permission_classes = []

    def get(self, request):
        return Response({"status": "ok"})


class ReadyView(APIView):
    permission_classes = []

    def get(self, request):
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return Response({"status": "ready"})


class DepsView(APIView):
    permission_classes = []

    def get(self, request):
        cache = redis.Redis(host=settings.REDIS_HOST, port=int(settings.REDIS_PORT), db=0)
        cache.ping()
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            cursor.fetchone()
        return Response({"database": "ok", "redis": "ok"})
