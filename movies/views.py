from django.db import models
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Movie, Actor
from .serializers import MovieSerializer, MovieDetailSerializer, ReviewCreateSerializer, CreateRatingSerializer, \
    ActorListSerializer, ActorDetailSerializer
from .service import get_client_ip


class MovieListView(generics.ListAPIView):
    serializer_class = MovieSerializer

    def get_queryset(self):
        movies = Movie.objects.filter(draft=False).annotate(
            rating_user=models.Case(
                models.When(ratings__ip=get_client_ip(self.request), then=True),
                default=False,
                output_field=models.BooleanField()
            ),
        )
        return movies


class MovieDetailView(generics.RetrieveAPIView):
    serializer_class = MovieDetailSerializer
    queryset = Movie.objects.get(draft=False)



class ReviewCreateView(APIView):
    def post(self, request):
        review = ReviewCreateSerializer(data=request.data)
        if review.is_valid():
            review.save()
        return Response(status=201)


class AddStarRatingView(APIView):
    def post(self, request):
        serializer = CreateRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(ip=get_client_ip(request))
            return Response(status=201)
        else:
            return Response(status=400)


class ActorListView(generics.ListAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorListSerializer


class ActorDetailView(generics.RetrieveAPIView):
    queryset = Actor.objects.all()
    serializer_class = ActorDetailSerializer