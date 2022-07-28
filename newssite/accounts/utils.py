from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six

class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        print("user.pk",user, user.pk)
        return (six.text_type(user.pk)+six.text_type(timestamp)+six.text_type(user.is_active))

tokenGenerator = TokenGenerator()