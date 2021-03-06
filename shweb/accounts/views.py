"""
.. module:: shweb.accounts
   :platform: Unix, Windows
   :synopsis: Module with views for accounts.

"""

from django.views import generic
from django.shortcuts import redirect
from django.contrib import messages
from django.http import Http404
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
UserModel = get_user_model()

from accounts.forms import CustomUserCreationForm
from accounts.utils import code_generator


def password_reset_done(request):
    """View which users request after reset password

    Args:
        request: Django request object

    Returns:
        Django http redirect object to designer create view.
    """
    messages.info(
        request,
        u"Check your email for further instructions")
    return redirect('designer:create')


def password_reset_complete(request):
    """View which users request after successful password change

    Args:
        request: Django request object

    Returns:
        Django http redirect object to login view
    """
    messages.info(
        request,
        u"Your password has been changed. You can log in now.")
    return redirect('login')


class RegistrationView(generic.FormView):
    """Users registration view
    """
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm
    success_url = 'designer:create'

    def form_valid(self, form):
        """Method trigered when form is valid. It assigns random confirmation
        code to user object.self

        Args:
            form: valid registartion form object

        Returns:
            Django http redirect object to success url
        """
        user = form.save()
        user.confirmation_code = code_generator()
        user.save()
        messages.info(self.request, "Thank you for registartion. We sent "
                      "you an email with confirmation link.")

        subject = "Account activation"
        from_mail = "sh-miR designer <shmir@brzeczkowski.pl>"
        to = [user.email]
        html_content = u"""<html>Click on the link to activate your account:
                       <a href="http://{0}{1}">
                       {0}{1}</a></html>
                       """.format(
            # self.request.get_host(),
            settings.SHMIR_HOST,
            reverse('accounts:confirm', kwargs={'code': user.confirmation_code})
        )
        msg = EmailMultiAlternatives(subject, html_content, from_mail, to)
        msg.content_subtype = 'html'
        msg.send()
        return redirect(self.success_url)


class AccountConfirmation(generic.View):
    """Account confirmation view (with confirmation code).
    """
    success_url = 'login'

    def get(self, *args, **kwargs):
        """Method for handling Http GET request. It checks if the user
        with given confirmation code exists and actives his/her account.

        Returns:
            Django http redirect object to success url

        Raises:
            Http404
        """
        code = kwargs.get('code')
        if code is None:
            raise Http404()

        try:
            user = UserModel.objects.get(confirmation_code=code)
        except UserModel.DoesNotExist:
            raise Http404()

        user.is_active = True
        user.save()
        messages.success(self.request, "Your account is active. Please log in.")
        return redirect(self.success_url)
