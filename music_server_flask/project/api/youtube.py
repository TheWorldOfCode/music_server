from flask import Blueprint, request
from flask_cors import cross_origin

import project.youtube as youtube
from project import task_manager

youtube_blueprint = Blueprint("youtube", __name__)


@youtube_blueprint.route("/api/youtube/search", methods=["POST"])
@cross_origin(origin="*", headers=['Content-Type'])
def queue_youtube():
    """ Search youtube for queue """
    queue = request.json['queue']
    limit = request.json['limit']

    results = youtube.Search(queue, limit)

    return {"data": results}

@youtube_blueprint.route("/api/youtube/download", methods=["POST"])
@cross_origin(origin="*", headers=['Content-Type'])
def download_youtube():
    url = request.json['url']
    type = request.json['type']
    title = request.json['title']
    
    task = youtube.download.delay(url, type)
    task_manager.add_task(task.id, title)

    return {}