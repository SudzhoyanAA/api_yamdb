from rest_framework import mixins, viewsets


class ListCreateDestroyViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    pass


class ExcludePutViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'head', 'options', 'patch', 'delete']


class CreateViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    pass
