from rest_framework import serializers

from tickets.models import Ticket
from users.serializers import UserDetailSerializer


class TicketCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['id', 'resource', 'reason', 'period', 'is_approved', 'user']


class TicketSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = Ticket
        fields = ['id', 'resource', 'reason', 'period', 'is_approved', 'user']
