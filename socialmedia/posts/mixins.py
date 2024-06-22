from django.db.models import Count


class LikedDislikedMixin():
    def number_of_likes(self):
        return Count(self.likes)

    def number_of_dislikes(self):
        return Count(self.dislikes)

    def liked_by(self, user):
        return self.likes.filter(pk=user.pk).exists()

    def disliked_by(self, user):
        return self.dislikes.filter(pk=user.pk).exists()
