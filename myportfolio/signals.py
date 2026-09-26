from django.contrib.auth.models import Group, Permission

def create_group_permissions(sender, **kwargs):
    try:
        # create groups
        readers_group, created = Group.objects.get_or_create(name="Readers")
        editors_group, created = Group.objects.get_or_create(name="Editors")

        # create permissions
        readers_permissions = [
            Permission.objects.get(codename="view_project")
        ]
        can_publish, created = Permission.objects.get_or_create(codename="publish_project", content_type_id=7, name = "Can Publish Project")
        editors_permissions = [        
            can_publish,
            Permission.objects.get(codename="add_project"),
            Permission.objects.get(codename="view_project"),
            Permission.objects.get(codename="change_project"),
            Permission.objects.get(codename="delete_project")
        ]

        # Assigning the permissions to groups
        readers_group.permissions.set(readers_permissions)
        editors_group.permissions.set(editors_permissions)

        print("Groups and Permissions Created Successfully!")
    except Exception as e:
        print(f"An error occured {e}")