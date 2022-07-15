from django.contrib.auth.models import Permission, Group
from django.contrib.contenttypes.models import ContentType


def run():

    # Generando permisos personalizados
    permissions = [
        {'name': 'Can associate risks to crisis scenarios', 'codename': 'associate_risks_to_crisisscenario', 'content_type_id': 'crisisscenario'},
        {'name': 'Can associate staffs to services offered', 'codename': 'associate_staffs_to_serviceoffered', 'content_type_id': 'serviceoffered'},
        {'name': 'Can associate risks to services offered', 'codename': 'associate_risks_to_serviceoffered', 'content_type_id': 'serviceoffered'},
        {'name': 'Can associate services offered to services used', 'codename': 'associate_servicesoffered_to_serviceused', 'content_type_id': 'serviceused'},
        {'name': 'Can associate risks to services used', 'codename': 'associate_risks_to_serviceused', 'content_type_id': 'serviceused'},
    ]
    for p in permissions:
        content_type_id = ContentType.objects.get(model=p['content_type_id']).id
        p['content_type_id'] = content_type_id
        p_obj, created = Permission.objects.get_or_create(**p)
        if created:
            print(f'Permiso {p["name"]} creado')
        else:
            print(f'Permiso {p["name"]} no creado')
