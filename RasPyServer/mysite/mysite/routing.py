from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import getData.routing

application = ProtocolTypeRouter({
	    'websocket': URLRouter(
            getData.routing.websocket_urlpatterns
        ),

    # (http->django views is added by default)
})


