from models import Post, Tag, Author


def latest_post(request):
    return {
        'latest_post': Post.objects.latest('created')
    }


def all_tags(request):
    return {
        'all_tags': Tag.objects.all()
    }


def all_authors(request):
    return {
        'all_authors': Author.objects.all()
    }


# def post_dates(request):
#     years = Post.objects.distinct('created__date')
#
#         # .dates('created', 'month')
#     # for year in years:
#     #     print Post.objects.filter(created=posts).dates('created', 'month')
#     print years
#     return {
#         'post_dates': Post.objects.dates('created','year').order_by('-created')
#     }