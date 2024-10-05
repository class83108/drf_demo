from rest_framework.throttling import UserRateThrottle


class WorkspaceThrottle(UserRateThrottle):
    THROTTLE_RATES = {"user": "5/day"}
