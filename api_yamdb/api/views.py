from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from django.shortcuts import render
from reviews.models import Category, Genre, Review, Title, User
from .serializers import TitleSerializer, CommentSerializer, ReviewSerializer




class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('-year')
    serializer_class = TitleSerializer
    permission_classes = (
        
    )

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    #написать пермишены
    permission_classes = (
        
    )
    
    def get_title(self):
        return get_object_or_404(Title, id=self.kwargs.get("title_id"))

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_title())
    

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        
    )

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get("review_id"))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
