from localflavor.us.us_states import STATES_NORMALIZED
from analytics.models import Ad


def location(request):
    return {
        'location': request.location
    }


# def state_ads(request):
#     if request.location['region'] is not None:
#         return {
#             'ad': Ad.objects.filter(state=STATES_NORMALIZED[request.location['region'].encode().lower()]).order_by('?')[0]
#         }
#     else:
#         pass