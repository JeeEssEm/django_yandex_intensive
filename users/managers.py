from django.contrib.auth.models import (
    UserManager as AbstractUserManager
)


class UserManager(AbstractUserManager):

    def get_active_users(self):
        return self.get_queryset().filter(
            is_active=True
        ).only('username', 'id')

    def get_user_detail(self, pk):
        return self.get_active_users().filter(
            pk=pk
        ).select_related('profile').only(
            'first_name',
            'last_name',
            'profile__image',
            'profile__birthday',
            'profile__coffee_count'
        )
