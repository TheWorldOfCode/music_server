function play(object) {
    console.log(object);
    $.getJSON('/player_control', {status: "play"}, function(data) {
        console.log(data);
        object.innerHTML = data["status"];
    }); 
}

function prev() {
    $.getJSON('/player_control', {status: "prev"}, function(data) {}); 
}

function next() {
    $.getJSON('/player_control', {status: "next"}, function(data) {}); 
}

function suffle() {
    $.getJSON('/player_control', {status: "suffle"}, function(data) {}); 
}

function random() {
    $.getJSON('/player_control', {status: "random"}, function(data) {}); 
}

function repeat() {
    $.getJSON('/player_control', {status: "repeat"}, function(data) {}); 
}

function consume() {
    $.getJSON('/player_control', {status: "consume"}, function(data) {}); 
}

function clear() {
    console.log("ENTER");
    $.getJSON('/player_control', {status: "clear"}, function(data) {console.log(data);}); 
    
}

function get_song() {
    $.getJSON('/status', {action: "song"}, function(data) {
        if (data.status == "stop") 
            document.getElementById("play_control").innerHTML = "Play";
        else if (data.status == "play")
            document.getElementById("play_control").innerHTML = "Pause";

        else
            document.getElementById("play_control").innerHTML = "Play";
        data = data.song
        var display = document.getElementById("player_status");
        var str = "<h1>";
        if (typeof data.title === "undefined") {
            str += "No song playing</h1>";
        } else {

            if (typeof data.track !== "undefined") {
                str += data.track + " - ";
            }

            str += data.title + "</h1>\n<p>";

            if (typeof data.album !== "undefined") {
                str += data.album + " - "; 
            }

            str += data.artist + "</p>";
        }

        display.innerHTML = str;
    });
}

function downloading_status() {
    $.getJSON('/status', {action: "downloading"}, function(data) {
        var running = document.getElementById("download_status");
        var done = document.getElementById("download_done");

        running.innerHTML = data.running;
        done.innerHTML = data.finished;
        
        if (window.location.pathname == "/youtube_downloader" ) {
            var info = document.getElementById("download_queue");
            var str = "";

            if (data.finished != "0") {
                str += "<h1>Downloads</h1>";

                for (var i = 0; i < data.info.length; i++) {
                    str += "<div class=\"hit\"><h1>";
                    str += data.info[i][0];
                    str += "<button class=\'btn btn-default\' onclick=\"open_tag_editor(" + data.info[i][1] + ")\">Contiune</button>";
                    str += "</h1></div>";
                }
            }
            info.innerHTML = str;
        
        }
    });

}

function get_playlist_name() {
    var name = document.getElementById("playlist_name");
    if (name != null) {
        $.getJSON('/status', {action: "playlist"}, function(data) {
            name.innerHTML = data.name;
        });
    }
}

function update() {
    get_song();
    get_playlist_name();
    downloading_status();
}

function extract_song_information(info) {
    return [info['track'], info['title']]
}

function add(item) {
    $.getJSON('/queue', {type: "add", info: item.id}, function(data) {
        document.getElementById("Status").innerHTML = "<p>" + data['data'] + "</p>";
    }); 
}

function remove(item) {
    $.getJSON('/queue', {type: "remove", info: item.id}, function(data) {
        document.getElementById("Status").innerHTML = "<p>" + data['data'] + "</p>";
        item.parentElement.innerHTML = "";
    }); 
}

function playlist_play_song(song_id) {
    // Play the clicked song
    $.getJSON('/player_control', {status: 'playlist', action: "play", song: song_id}, function(data) {
    }); 

    // Show that the show is beging played
    var current_song = document.getElementsByClassName("current")[0];
    current_song.classList.remove("current");
    document.getElementById("song_id-" + song_id).classList.add("current");

}

function playlist_remove_song(song_id) {
    $.getJSON('/player_control', {status: 'playlist', action: "remove", song: song_id}, function(data) {}); 
    var row = document.getElementById("song_id-" + song_id);
    row.parentNode.removeChild(row);

}

function popup(row) {
    var popup = document.getElementsByClassName("popuptext");
    for (var i = 0; i < popup.length; i++) {
        popup[i].classList.remove("show");
    }
    row.getElementsByClassName("popuptext")[0].classList.toggle("show");
}


function downloader_search() {
    var input = document.getElementById("search");
    var display = document.getElementById("result");
    var queue = input.value;
    $.getJSON('/youtube_downloader_control', {action: 'search', queue: queue, hits: 2}, 
        function(result) {
            var str = "";
            var list = result.result;

            for (var i = 0; i < list.length; i++) {
                if (typeof list[i] === "undefined")
                    continue;
                str += "<div class=\"hit\">";
                str += "<h1>Title: " + list[i].title + "</h1>";
                if (list[i].type == "video") {
                    str += "<h3>Duration: " + list[i].duration + "</h3>";
                } else {
                    str += "<h3>Tracks: " + list[i].count + "</h3>";
                }
                str += "<p>Type: " + list[i].type + "\nUrl: " + list[i].url + "</p>";
                str += "<button class=\'btn btn-default\' onclick=\'youtube_download(\"" + list[i].type + "\", \""+ list[i].url + "\", \"" + list[i].title + "\")\'>Download</button>";
                str += "</div>";
            }

            display.innerHTML = str;
        }); 
}

function youtube_download(type, url, title) {
    $.getJSON("/youtube_downloader_control", {action: "download", type: type, url: url, queue: title}, function(result) { });
}

function open_tag_editor(id) {
    console.log(id);
    $.getJSON("/youtube_downloader_control", {action: "tag_editor", id: id}, function(result) { console.log(result); tag_editor(result); });
}

function tag_editor(result){
    var editor = document.getElementById("tageditor");
    var content = editor.getElementsByClassName("modal-content")[0];
    var type = result.type;
    var html = ""
    html +=  "<h1>" +  result.queue + "</h1>";
    if (type == "video"){
        var new_title = result.title.replace(/[\[|\(][a-zA-Z0-9 ]+[\]|\)]/g, "");
        html +=  "<label>Title:</label> <input id=\"title\" type=\"text\" value=\"" + new_title + "\"><p></p>";
        html +=  "<label>Artist:</label> <input id=\"artist\" type=\"text\" value=\"" + result.artist +"\"><p></p>";
        html +=  "<label>Album:</label> <input id=\"album\" type=\"text\" value=\"\"><p></p>";
        html +=  "<label>Track:</label> <input id=\"track\" type=\"text\" value=\"\"><p></p>";
        html += "<span id=\"" + result.filename + "\"></span>";
    } else {
        var data = result;
        var artist = data[0].artist;
        var album = data[0].album;
        html +=  "<label>Artist:</label> <input id=\"artist\" type=\"text\" value=\"" +  artist +"\"><p></p>";
        html +=  "<label>Album:</label> <input id=\"album\" type=\"text\" value=\"" + album +"\"><p></p>";
        html +=  "<ul>";
        var re = new RegExp(artist + "[ -]+");
        var filenames = "";
        for (var i = 0; i < data.length; i++) {
            var title = data[i].title.replace(re, "").replace(/\[OFFICAL VIDEO\]/i,"");
            html += "<li><label>Track: </label><input id=\"track\" type=\"text\" value=\"" + data[i].track + "\"> <label> Title: </label><input id=\"title\" type=\"text\" value=\"" + title + "\"></li>"
            filenames += data[i].filename + ",";
        }
        html +=  "</ul>";
        html += "<span id=\"" + filenames + "\"></span>";

    }
    html += "<button class=\"btn btn-default\" onclick=\'youtube_done(\"" + type + "\")\'>Done</button>"
    content.innerHTML = html;

    editor.style.display = "block";

}

function youtube_done(type) {
    var editor = document.getElementById("tageditor");
    var content = editor.getElementsByClassName("modal-content")[0];

    if (type == "video") {
        var info = new Array(1);
        var list = content.getElementsByTagName("input");
        var title = list[0].value;
        var album = list[2].value;
        var artist = list[1].value;
        var track = list[3].value;
        var filename = content.getElementsByTagName("span")[0].id;

        info[0] = {"artist": artist, "album": album, "filename": filename, "track": track, "title": title};
        $.getJSON("/youtube_downloader_control", {action: "tag", "type": type, "details": JSON.stringify(info)}, function(result) { });

    } else {
        var list = content.getElementsByTagName("input");
        var filenames = content.getElementsByTagName("span")[0].id.split(",");
        var artist = list[0].value;
        var album = list[1].value;

        var info = new Array(list.length - 2);

        var j = 0;
        for (var i = 2; i < list.length; i+=2) {
            info[j] = {"artist": artist, "album": album, "filename": filenames[j], "track": list[i].value, "title": list[i+1].value};
            j += 1;
        }

        $.getJSON("/youtube_downloader_control", {action: "tag", "type": type, "details": JSON.stringify(info)}, function(result) {
        });

    }

    editor.style.display = "none";
}


function save_playlist() {
    var name = document.getElementById("playlist_name").innerHTML;

    $.getJSON("/player_control",  {status: "save", name: name}, function(data) {});
}
