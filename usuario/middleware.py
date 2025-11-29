from .models import Usuario

class UserInfoMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        usuario_id = request.session.get('usuario_id')
        # Inicializamos valores por defecto en cada request
        request.usuario = None
        request.user_is_admin = False
        request.user_is_ayudante = False

        if usuario_id:
            try:
                usuario = Usuario.objects.get(id=usuario_id)
                # Adjuntamos el objeto de usuario completo para fácil acceso
                request.usuario = usuario
                # Adjuntamos roles para verificaciones rápidas
                request.user_is_admin = usuario.es_admin
                request.user_is_ayudante = usuario.es_ayudante
            except Usuario.DoesNotExist:
                # Si el usuario_id en la sesión es inválido, lo limpiamos para evitar errores.
                del request.session['usuario_id']

        response = self.get_response(request)
        return response