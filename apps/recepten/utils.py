import os
from django.contrib import messages
from django.db.models.deletion import RestrictedError
from django.shortcuts import redirect, render, get_object_or_404

def handle_delete(request, model, pk, success_url, template_name, object_name=None):
    """
    Algemene delete-handler die RestrictedError opvangt en messages toont.

    Parameters:
    - request: Django request object
    - model: Model class (bijv. Categorie)
    - pk: primary key van het object
    - success_url: url-naamstring waarnaar geredirect wordt bij succes
    - template_name: template voor confirm delete
    - object_name: optioneel, naam voor messages (default: str(object))
    """
    obj = get_object_or_404(model, pk=pk)
    display_name = object_name or str(obj)

    if request.method == "POST":
        try:
            obj.delete()
            messages.success(request, f"{display_name} is verwijderd.")
            return redirect(success_url)
        except RestrictedError:
            messages.error(
                request,
                f"{display_name} kan niet worden verwijderd omdat het nog gebruikt wordt in één of meer recepten."
            )
            return redirect(request.path)

    return render(request, template_name, {"object": obj})

def recept_image_path(instance, filename):
    # Haal bestandsextensie van de upload
    ext = filename.split('.')[-1]
    # Maak receptnaam "veilig" (spaties → underscores, lowercase)
    safe_name = instance.naam.replace(" ", "_").lower()
    # Bestandsnaam is gewoon de receptnaam met juiste extensie
    filename = f"{safe_name}.{ext}"
    # Opslag in submap per recept
    return os.path.join('recepten/images', safe_name, filename)