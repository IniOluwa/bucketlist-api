from . import main
from .. import db
from ..models import BucketList, BucketListItem
from flask import request, jsonify, abort, g
from .authentication import auth


@main.route('/', methods=['GET', 'POST'])
def index():
    return "The app works!"


@auth.login_required
@main.route('/bucketlists/', methods=['GET', 'POST'])
def create_and_get_bucketlists():
    if request.method == 'POST':
        name = request.json.get('name')
        if name is None:
            abort(400)
        bucketlist = BucketList(name=name)
        bucketlist.save()
        return jsonify(bucketlist.to_json())
    # elif request == 'POST':
    #     pass


@main.route('/bucketlists/<int:id>', methods=['GET', 'PUT', 'DELETE'])
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
def create_bucketlistitem(id):
    name = request.json.get('name')
    item = BucketListItem(name=name)
    item.save()
    return jsonify({
        'item': item.to_json(),
        'message': 'Bucket list item has been successfully created'
    })


@main.route('/bucketlists/<id>/items/<int:item_id>', methods=['PUT', 'DELETE'])
def edit_delete_bucketlistitem(id, item_id):
    bucketlistitem = BucketListItem.query.get(item_id)
    if request.method == 'PUT':
        name = request.json.get('name')
        bucketlistitem.done = True
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
