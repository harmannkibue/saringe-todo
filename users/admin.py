from django.contrib import admin
from django.apps import apps
from django.contrib.admin.sites import AlreadyRegistered
from oauth2_provider.admin import Application
from saringe_todo import settings
from users.models import User

app_models = apps.get_app_config('users').get_models()

for model in app_models:
    try:
        attrs = {"list_display": [f.name for f in model._meta.get_fields() if not f.many_to_many and not f.one_to_many]}
        name = "Admin_" + model.__name__
        theclass = type(str(name), (admin.ModelAdmin,), attrs)
        admin.site.register(model, theclass)
    except AlreadyRegistered:
        pass


if settings.DEBUG is True:
    try:
        client_id = "iuyutyutuyctub"
        client_secret = "lahkckagkegigciegvjegvjhd"
        user=None

        if User.objects.filter(username="myadmin").exists():
            print("The myadmin already exists")
            user = User.objects.get(username="myadmin")
            user.is_staff = True
            user.is_superuser = True
            user.save()
            pass
        else:
            print("Creating super myadmin for test...")
            user = User.objects.create_user(username="myadmin", email="myadmin@gmail.com", password="#myadmin")
            user.is_staff = True
            user.is_superuser = True
            user.save()

        ##Myadmin
        try:
            app = Application()
            app.name="Dev (To be deleted...)"
            app.client_id = client_id
            app.user = user
            app.authorization_grant_type = "password"
            app.client_type = "public"
            app.client_secret = client_secret
            if not Application.objects.filter(client_id=client_id).exists():
                app.save()
        except Exception as e:
            print(e)
    except:
        pass

