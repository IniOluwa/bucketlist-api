from . import main
from .. import db
from ..models import User, BucketList, BucketListItem


@main.route('/', methods=['GET', 'POST'])
def index():
    return "The app works!"
