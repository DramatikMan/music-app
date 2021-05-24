# from functools import wraps

from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Room
from .serializers import (
    RoomSerializer,
    RoomCreateSerializer,
    UpdateRoomSerializer
)


# def session_required(func):
#     ''' Check if session key exists in session, create session otherwise '''
#     @wraps(func)
#     def wrapper(*args, **kwargs):
#         if not self.request.session.exists(self.request.session.session_key):
#             self.request.session.create()
#         func(*args, **kwargs)
#         return wrapper


class Rooms(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer


class GetRoom(APIView):
    serializer_class = RoomSerializer

    def get(self, request, format=None):
        code = request.GET.get('code')

        if code:
            queryset = Room.objects.filter(code=code)

            if queryset.exists():
                data = RoomSerializer(queryset[0]).data
                data['is_host'] = \
                    self.request.session.session_key == queryset[0].host
                return Response(data, status=status.HTTP_200_OK)

            return Response(
                {'Room Not Found': 'Invalid Room code.'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        return Response(
            {'Bad Request': 'Key "code" not found in request.'},
            status=status.HTTP_400_BAD_REQUEST
        )


class JoinRoom(APIView):
    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        code = request.data.get('code')

        if code:
            queryset = Room.objects.filter(code=code)

            if queryset.exists():
                room = queryset[0]
                self.request.session['room_code'] = code
                return Response(
                    {'Message': 'Room joined!'},
                    status=status.HTTP_200_OK
                )

            return Response(
                {'Room Not Found': 'Invalid Room code.'},
                status=status.HTTP_404_NOT_FOUND
            )
                
        return Response(
            {'Bad Request': 'Key "code" not found in request.'},
            status=status.HTTP_400_BAD_REQUEST
        )


class CreateRoom(APIView):
    serializer_class = RoomCreateSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')
            host = self.request.session.session_key

            room, created = Room.objects.update_or_create(
                host=host, 
                defaults=dict(
                    guest_can_pause=guest_can_pause,
                    votes_to_skip=votes_to_skip
                )
            )
            self.request.session['room_code'] = \
                RoomSerializer(room).data['code']

            if created:
                return Response(
                    RoomSerializer(room).data,
                    status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    RoomSerializer(room).data,
                    status=status.HTTP_200_OK
                )

        return Response(
            {'Bad Request': 'Invalid data.'},
            status=status.HTTP_400_BAD_REQUEST
        )


class UserInRoom(APIView):
    def get(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        data = {'code': self.request.session.get('room_code')}
        return JsonResponse(data, status=status.HTTP_200_OK)


class LeaveRoom(APIView):
    def put(self, request, format=None):
        if 'room_code' in self.request.session:
            self.request.session.pop('room_code')

            host_id = self.request.session.session_key
            queryset = Room.objects.filter(host=host_id)

            if queryset.exists():
                room = queryset[0]
                room.delete()

        return Response({'Message': 'Success.'}, status=status.HTTP_200_OK)


class UpdateRoom(APIView):
    serializer_class = UpdateRoomSerializer

    def patch(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            code = serializer.data.get('code')
            guest_can_pause = serializer.data.get('guest_can_pause')
            votes_to_skip = serializer.data.get('votes_to_skip')

            queryset = Room.objects.filter(code=code)

            if not queryset.exists():
                return Response(
                    {'Message': 'Room Not Found.'},
                    status=status.HTTP_404_NOT_FOUND
                )

            room = queryset[0]
            user_id = self.request.session.session_key

            if room.host != user_id:
                return Response(
                    {'Forbidden': 'You are not the host.'},
                    status=status.HTTP_403_FORBIDDEN
                )

            room.guest_can_pause = guest_can_pause
            room.votes_to_skip = votes_to_skip
            room.save(update_fields=['guest_can_pause', 'votes_to_skip'])

            return Response(
                RoomSerializer(room).data,
                status=status.HTTP_200_OK
            )

        return Response(
            {'Bad Request': 'Invalid data.'},
            status=status.HTTP_400_BAD_REQUEST
        )