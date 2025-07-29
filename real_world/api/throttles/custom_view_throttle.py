from rest_framework.throttling import UserRateThrottle

class CustomViewThrottle(UserRateThrottle):
    scope = 'custom_view'
