# maze/migrations/0002_prepopulate_categories.py

from django.db import migrations

def create_categories_and_subcategories(apps, schema_editor):
    Category = apps.get_model('maze', 'Category')
    SubCategory = apps.get_model('maze', 'SubCategory')

    # Define categories and their subcategories
    categories = {
        'Engineering': ['Mechanical', 'Automotive', 'Electrical', 'Civil', 'Plumbing'],
        'IT': ['Software Development', 'Cybersecurity', 'Network Administration'],
        'Marketing': ['Digital Marketing', 'Content Marketing', 'SEO'],
        'Others': ['Consulting', 'Design', 'Support'],
    }

    for category_name, subcategories in categories.items():
        category, created = Category.objects.get_or_create(name=category_name)
        for sub_name in subcategories:
            SubCategory.objects.get_or_create(name=sub_name, category=category)

class Migration(migrations.Migration):

    dependencies = [
        ('maze', '0001_initial'),  # Ensure this matches your initial migration
    ]

    operations = [
        migrations.RunPython(create_categories_and_subcategories),
    ]
