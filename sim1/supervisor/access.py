from .modeles import SupervisorUtilisateur  # Assuming model name is 'SupervisorUtilisateur'
from django.shortcuts import redirect
from django.http import HttpRequest

def get_full_path(request: HttpRequest) -> str:
    """Constructs the full URL for the current request.

    Args:
        request (HttpRequest): The Django request object.

    Returns:
        str: The complete URL of the current request.
    """

    return f"{request.scheme}://{request.get_host()}{request.path}"



class RoleDispatcher:

    def __init__(self):
        self.role_mappings = {
            'gestionnaire': 'gestionH',
            'vendeur': 'vente_home',
            'superviseur': 'home_supervisor',
        }

    def dispatch(self, request):
        if request.user.is_authenticated:
            try:
                person = SupervisorUtilisateur.objects.get(id=request.user.id)
                redirect_url = self.role_mappings.get(person.role)

                # Check if current URL matches the role's URL
                current_url = get_full_path(request)
                if current_url == redirect_url:
                    
                    return None  
                else:
                    
                    return redirect(redirect_url)

            except SupervisorUtilisateur.DoesNotExist:
                
                return redirect('login')

        else:
            return redirect('login')

        
