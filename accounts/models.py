from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    def get_serialized(self):
        return {
            'id': self.id,
            'email': self.email,
        }
