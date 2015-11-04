from . import main
from ..models import BucketList, BucketListItem
from flask import request, jsonify, abort, g, url_for
from .authentication import auth


@main.route('/bucketlists/', methods=['GET', 'POST'])
@auth.login_required
def create_and_get_bucketlists():
    if request.method == 'POST':
        name = request.json.get('name')
        if name is None:
            abort(400)
        bucketlist = BucketList(
            name=name, created_by=g.user.username, author=g.user)
        bucketlist.save()
        return jsonify(bucketlist.to_json())

    elif request.method == 'GET':
        # import pdb; pdb.set_trace()

        bucketlists = BucketList.query.filter_by(author=g.user)

        page = request.args.get('page', 1, type=int)
        page_max = request.args.get('limit', 20, type=int)
        
        q = request.args.get('q', type=str)
        if q:
            bucketlists = bucketlists.filter(BucketList.name.ilike('%{0}%'.format(q)))

        pagination = bucketlists.paginate(page, page_max, False)
        pages = pagination.items

        prev_page = None
        if pagination.has_prev:
            prev_page = url_for( 'main.create_and_get_bucketlists', page=page-1, _external=True)

        next_page = None
        if pagination.has_next:
            next_page = url_for( 'main.create_and_get_bucketlists', page=page+1, _external=True)
        return jsonify({
            'bucketlist': [page_object.to_json() for page_object in pages],
            'previous': prev_page,
            'next': next_page
        })


@main.route('/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
@auth.login_required
def get_edit_delete_bucketlist(id):
    bucketlist = BucketList.query.get(id)
    if request.method == 'GET':
        if bucketlist is None:
            return jsonify({
                'message': 'This bucketlist is not available.'
            })
        return jsonify(bucketlist.to_json())

    elif request.method == 'PUT':
        name = request.json.get('name')
        bucketlist.edit(name)
        bucketlist.save()
        return jsonify(bucketlist.to_json()), 201

    elif request.method == 'DELETE':
        bucketlist.delete()
        return jsonify({
            'message': 'The Bucketlist has been successfully deleted.'
        })


@main.route('/bucketlists/<int:id>/items', methods=['POST'])
@auth.login_required
def create_bucketlistitem(id):
    if request.method == 'POST':
        bucketlist = BucketList.query.get(id)
        name = request.json.get('name')
        if bucketlist is None:
            abort(400)
        item = BucketListItem(name=name, bucketlist=bucketlist)
        item.save()
        return jsonify({
            'item': item.to_json(),
            'message': 'Bucket list item has been successfully created'
        })


@main.route('/bucketlists/<int:id>/items/<int:item_id>', methods=['PUT', 'DELETE'])
@auth.login_required
def edit_delete_bucketlistitem(id, item_id):
    bucketlistitem = BucketListItem.query.get(item_id)
    if request.method == 'PUT':
        name = request.json.get('name')
        bucketlistitem.edit(name)
        bucketlistitem.save()
        return jsonify({
            'item': bucketlistitem.to_json(),
            'message': 'Bucket list item has been successfully changed'
        })
    elif request.method == 'DELETE':
        bucketlistitem.delete()
        return jsonify({
            'message': 'The Bucket list item has been successfully deleted.'
        })
