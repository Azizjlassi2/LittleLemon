from rest_framework.throttling import SimpleRateThrottle,UserRateThrottle




class CustomerRateThrottle(SimpleRateThrottle):

    scope= "customer" 



    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated and   request.user.groups.filter(name="Manager").exists() and  request.user.groups.filter(name="Delivery Crew").exists():
            ident = request.user.pk
        else:
            return None

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
    
    

class ManagerRateThrottle(SimpleRateThrottle):


    scope = 'manager'

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated and request.user.groups.filter(name="Manager").exists():
            ident = request.user.pk
        else:
            return None

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }
    



class DeliveryCrewRateThrottle(SimpleRateThrottle):


    scope = 'delivery-crew'

    def get_cache_key(self, request, view):
        if request.user and request.user.is_authenticated and request.user.groups.filter(name="Delivery Crew").exists():
            ident = request.user.pk
        else:
            return None
        

        return self.cache_format % {
            'scope': self.scope,
            'ident': ident
        }