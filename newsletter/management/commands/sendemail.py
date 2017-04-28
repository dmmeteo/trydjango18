from django.core.management.base import BaseCommand, CommandError
from newsletter.models import SignUp
from optparse import make_option
from django.conf import settings
from django.core.mail import send_mail


class Command(BaseCommand):
    args = '<email email ...>'
    help = 'Test management command'
    option_list = BaseCommand.option_list + (
        make_option('--test',
                    action='store_true',
                    dest='test',
                    default=False,
                    help='Send mail for <user> if he is exist'),
    )

    def handle(self, *args, **options):
        email_list = []
        for email in args:
            try:
                query = SignUp.objects.get(email=email)
            except SignUp.DoesNotExist:
                raise CommandError('User with email "%s" does not exist' % email)

            email_list.append(email)
            self.stdout.write('User name is "%s"' % query.full_name)

        subject = 'Hui manager'
        from_email = settings.EMAIL_HOST_USER
        to_email = [] + email_list
        contact_message = 'Bla-bla-bla text lorem text lol hui...'

        if len(email_list) and not options['test']:
            send_mail(subject,
                      contact_message,
                      from_email,
                      to_email,
                      fail_silently=False)
        else:
            self.stdout.write('Program "send_mail"\n from_email: %s\n to_email: %s\n subject: %s\n content: %s' % (from_email,
                                                                                                                   to_email,
                                                                                                                   subject,
                                                                                                                   contact_message)
                              )


