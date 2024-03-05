from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, viewsets
from django.shortcuts import render
from reviews.models import Category, Genre, Review, Title, User





class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('-year')
    serializer_class = TitleSerializer
    permission_classes = (
        IsAuthorOrReadOnly,
        IsAuthenticatedOrReadOnly,
    )

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    #написать пермишены
    permission_classes = (
        
    )

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
    

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = (
        IsAuthorOrReadOnly,
        IsAuthenticatedOrReadOnly,
    )

    def get_review(self):
        return get_object_or_404(Review, id=self.kwargs.get("review_id"))

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
