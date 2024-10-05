from rest_framework.throttling import UserRateThrottle, ScopedRateThrottle


class WorkspaceThrottle(UserRateThrottle):
    THROTTLE_RATES = {"user": "5/day"}


# 如果是要配置scope的話，可以這樣寫
class DocumentThrottle(ScopedRateThrottle):
    THROTTLE_RATES = {"document": "10/day"}
