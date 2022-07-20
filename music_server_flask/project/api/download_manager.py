from flask import Blueprint, request, jsonify
from flask_cors import cross_origin

import project.youtube as youtube
from project import task_manager, db
from project.database import Song
from os import remove

download_manager = Blueprint("download_manager", __name__)

@download_manager.route("/api/download/status", methods=["GET"])
@cross_origin(origin="*", headers=['Content-Type'])
def get_download_status():
    status =  task_manager.get_status()

    running = 0
    done = 0
    failed = 0
    for name, state in status:
        if state.lower() == "success":
            done += 1
        elif state.lower() == "failed":
            failed += 1 
        else:
            running += 1


    return {"running": running, "done": done, "failed": failed}

@download_manager.route("/api/download/downloaded", methods=["GET"])
@cross_origin(origin="*", headers=['Content-Type'])
def get_downloaded():
    """
        Get data for the downloaded tasks

        
        Response:
            data: The data from the successful downloaded songs
            failed: The data from the failed 
            
    """
    results = task_manager.get_results()
    failed = task_manager.get_results("failed")

    return {"data": results, "failed": failed}

@download_manager.route("/api/download/retry", methods=["POST"])
@cross_origin(origin="*", headers=['Content-Type'])
def retry_download():
    """
        Retry a download 
        @TODO NOT WORKING 

        Request:
            id: The task id of which to retry
    """
    
    id = request.json["id"]

    task_manager.retry(id)

    return {}

@download_manager.route("/api/download/add", methods=["POST"])
@cross_origin(origin="*", headers=['Content-Type'])
def add_download():
    """
        Finish the download by adding it to the database. 
        
        Request:
            data: The information for each song,
                title: The title of the song.
                artist: The artist of the song 
                album: The album the song belong to
                track: The track number 
                filename: The filename
            overwrite: Overwrite exists files
            new: If it is a new song
        
        Responce:
            success: If it worked. 
    """

    data = request.json["data"]
    id = request.json["id"]
    overwrite = request.json["overwrite"]

    for song in data:
        s = Song(song["title"], song["artist"], song.get("album", ""), 
                song.get("track", ""), song["filename"])

        try:
            s.check_filename(overwrite)    
        except:
            return {"success": False}

        s.update_tag()
        db.session.add(s)

    db.session.commit()

    task_manager.remove_task(id)

    return {"success": True}

@download_manager.route("/api/download/remove", methods=["POST"])
@cross_origin(origin="*", headers=['Content-Type'])
def remove_download():
    """ Remove download. It is only possible if the task is done or failed

        Request: 
            id: The task id 
        responce:
            success: If the task was removed

    """
    id = request.json["id"]

    result = task_manager.get_result(id)
    status = result.status

    if status.lower() == "success":
        remove(result.result.get("filename"))
        task_manager.remove_task(id)
    elif status.lower() == "failed":
        task_manager.remove_task(id)
    else:
        return {"success": False}

    return {"success": True}
