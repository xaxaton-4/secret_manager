from rest_framework import serializers

from tickets.models import Ticket
from users.serializers import UserDetailSerializer


class TicketSerializer(serializers.ModelSerializer):
    user = UserDetailSerializer()

    class Meta:
        model = Ticket
        fields = ['id', 'resource', 'reason', 'period', 'is_approved', 'user']
