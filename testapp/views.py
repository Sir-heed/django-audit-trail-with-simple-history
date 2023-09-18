from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet


from . import models, serializers


class RevertMixin:
    @action(
        methods=['GET'],
        detail=True,
        url_path='revert/(?P<history_id>[^/.]+)'
    )
    def revert_obj(self, request, history_id, pk=None):
        """revert obj to a particular change"""
        obj = self.get_object()
        try:
            hist = self.history_model.objects.get(id=obj.id, history_id=history_id)
        except self.history_model.DoesNotExist:
            return Response({'msg': 'History does not exist'}, status=status.HTTP_404_NOT_FOUND)
        hist.instance.save()
        obj.refresh_from_db()
        return Response(self.get_serializer(obj).data)


class PollViewSet(RevertMixin, ModelViewSet):
    model = models.Poll
    history_model = models.HistoricalPoll
    queryset = models.Poll.objects.filter(is_active=True)
    serializer_class = serializers.PollSerializer


class ChoiceViewSet(RevertMixin, ModelViewSet):
    model = models.Choice
    history_model = models.HistoricalChoice
    queryset = models.Choice.objects.filter(is_active=True)
    serializer_class = serializers.ChoiceSerializer


class HistoryMixin(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    @action(
        methods=['GET'],
        detail=True,
        url_path='next',
    )
    def next_history(self, request, pk=None):
        """get the next change"""
        obj = self.get_object()
        data = self.serializer_class(obj.next_record).data if obj.next_record else {}
        return Response(data) 

    @action(
        methods=['GET'],
        detail=True,
        url_path='prev',
    )
    def previous_history(self, request, pk=None):
        """get the previous change"""
        obj = self.get_object()
        data = self.serializer_class(obj.next_record).data if obj.next_record else {}
        return Response(data)


class PollHistoryViewSet(HistoryMixin):
    model = models.HistoricalPoll
    queryset = models.HistoricalPoll.objects.all()
    serializer_class = serializers.HistoricalPollSerializer


class ChoiceHistoryViewSet(HistoryMixin):
    model = models.HistoricalChoice
    queryset = models.HistoricalChoice.objects.all()
    serializer_class = serializers.HistoricalChoiceSerializer
