from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Message
from .serializers import MessageSerializer
import logging

logger = logging.getLogger(__name__)

class SendMessageView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        try:
            serializer = MessageSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()  # sender will be handled manually via request.data['sender']
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            logger.error(f"Message sending failed: {e}", exc_info=True)
            return Response(
                {"error": "Message sending failed", "message": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class MessageListView(APIView):
    # permission_classes = [IsAuthenticated]
    permission_classes = (AllowAny,)


    def get(self, request, *args, **kwargs):
        try:
            # Retrieve all messages sent or received by the user
            messages = Message.objects.filter(sender=request.user) | Message.objects.filter(receiver=request.user)
            serializer = MessageSerializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"Failed to retrieve messages: {e}", exc_info=True)
            return Response(
                {"error": "Failed to retrieve messages", "message": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
