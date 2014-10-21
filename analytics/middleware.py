from ipware.ip import get_real_ip
import requests
from analytics.models import Page, Location, View
from rocketu_blog_analytics import settings


class LocationMiddleware(object):
    def process_request(self, request):
        # Get the IP Address of this request
        ip = get_real_ip(request)

        # If we didn't get an IP Address and we're developing locally,
        # make an API call to get our IP Address.
        if ip is None and settings.DEBUG:
            ip = requests.get('http://icanhazip.com/').text

        if ip is not None:
            response = requests.get('http://ipinfo.io/{}/json'.format(ip))
            if response.status_code == 200:
                request.location = response.json()
                # Split out the lat and long from the location
                request.location['latitude'], request.location['longitude'] = request.location['loc'].split(',')

        request.ip = ip


class SaveViewMiddleware(object):
    def process_request(self, request):
        # print request.META['PATH_INFO']
        # print request.location['city'], request.location['region'], request.location['country']
        # print request.location['latitude'], request.location['longitude']
        path_list = request.META['PATH_INFO'].split('/')
        print request.META['PATH_INFO']
        print type(path_list[1])
        print path_list[1] == u'admin'
        print path_list[1] == u'analytics'
        if path_list[1] != u'admin' and path_list[1] != u'analytics':
            page, created = Page.objects.get_or_create(url=request.META['PATH_INFO'])
            location, created = Location.objects.get_or_create(city=request.location['city'],
                                                               region=request.location['region'],
                                                               country=request.location['country'])
            View.objects.create(ip_address=request.ip, page=page, location=location, latitude=request.location['latitude'],
                                longitude=request.location['longitude'])