from django.db import migrations

def create_default_admin(apps, schema_editor):
    # Use the historical version of the User model
    User = apps.get_model('auth', 'User')
    # Create the superuser
    User.objects.create_superuser(
        username='Hisham',
        email='Hisham@example.com',
        password='123456789',
        is_staff=True,  # Use boolean True instead of 1
    )

class Migration(migrations.Migration):
    dependencies = [
        # Add dependencies here (e.g., the initial migration of your app)
        # Ensure this migration runs after the auth app's migrations
        ('auth', '0001_initial'),  # Replace #### with the correct initial migration number for the auth app
    ]

    operations = [
        migrations.RunPython(create_default_admin),
    ]