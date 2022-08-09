<template>
<div id="MusicLibrary">

    <div class="viewer">
        <UploadFiles v-show="upload" @done="upload = false"/>
        <button class="btn btn-upload" @click="upload = true" v-show="!upload"> Upload </button>
        <ul v-for="(artist, index) in songs" :key="index">
            <li>
                <span class="artist" @click="artist.show=!artist.show">{{artist.name}}</span>
                <div v-show="artist.show">
                    <div v-if="Object.keys(artist.albums).length > 0">
                        <span>Albums:</span>
                        <ul v-for="(album, index2) in artist.albums" :key="index2">
                            <li class="li-music"> 
                                <span>{{index2}}</span> 
                                <button class="btn btn-list" @click="download_album(album)"> <i class="fa fa-download"></i></button> 
                                <button class="btn btn-list" @click="remove_album(album)"><i class="fa fa-trash"/></button>
                                <div>
                                    <ul v-for="song in album" :key="song.title">
                                        <li class="li-music">
                                            <span>{{song.track}} - {{song.title}}</span>
                                            <button class="btn btn-list" @click="download_file(song.filename)"><i class="fa fa-download"/></button>
                                            <button class="btn btn-list" @click="remove_song(song.song_id)"><i class="fa fa-trash"/></button>
                                            <button class="btn btn-list" @click="song.show = !song.show"><i class="fa fa-pencil"/></button>
                                            <Editor :info="[song]" :id="song.song_id.toString()" :library="true" @cancel-edit="song.show=false" @saved-edit="edited()" v-show="song.show"/> 
                                        </li>
                                    </ul>
                                </div>    
                            </li>
                        </ul>
                    </div>
                    <div v-if="artist.singles.length > 0">
                        <span>Singles:</span>
                        <ul v-for="song in artist.singles" :key="song.title">
                            <li class="li-music">
                                <span>{{song.title}}</span>
                                <button class="btn btn-list" @click="download_file(song.filename)"> <i class="fa fa-download"/></button>
                                <button class="btn btn-list" @click="remove_song(song.song_id)"><i class="fa fa-trash"/></button>
                                <button class="btn btn-list" @click="song.show = !song.show"><i class="fa fa-pencil"/></button>
                                <Editor :info="[song]" :id="song.song_id.toString()" :library="true" @cancel-edit="song.show=false" @saved-edit="edited()" v-show="song.show"/>
                            </li>
                        </ul>
                    </div>
                </div>
            </li>
            
        </ul>
    
    </div>
</div>
</template>

<script>
import axios from 'axios';
import Editor from "@/components/TagEditor.vue";
import UploadFiles from "@/components/UploadFiles.vue"

export default {
    components: {
    Editor,
    UploadFiles
},

    data() {
        return {
            songs: {},
            upload: false,
        };
       
    },

    async created() {
        this.get_songs()
    },

    methods: {
        async get_songs() {
            const path =  window.location.origin + "/api/library/songs"

            const responce = await axios.get(path, {})

            var information = responce.data.information

            for (let artist in information) {
                information[artist]["show"] = false

                for (var i = 0; i < information[artist]["singles"].length; i++) {
                    information[artist]["singles"][i]["show"] = false
                }

                for (let album in information[artist]["albums"]) {
                    for (i = 0; i < information[artist]["albums"][album].length; i++) {
                        information[artist]["albums"][album][i]["show"] = false
                    }
                }
            }
 
            this.songs = information
        //    console.log(this.songs)
        },

        async remove_album(album) {
            album.forEach((song) => {
                this.remove_song(song.song_id)
            })
        },

        async edited() {
            setTimeout(() => {this.get_songs()}, 100)
        },

        async remove_song(song_id) {
            const path = window.location.origin + "/api/library/delete/" + song_id
            axios.delete(path);

            this.get_songs()
        },

        download_album(album) {
            album.forEach((song) => {
                this.download_file(song.filename)
            })
        },

        download_file(filename) {

            filename = filename.replace("/tmp/", "")
            const path = window.location.origin + "/api/library/download/" + filename
            
            axios({
                method: "GET",
                url: path,
                responseType: "blob"
                }).then((res) => {
                var FILE = window.URL.createObjectURL(new Blob([res.data], { type: 'application/m4a' }));
                var docUrl = document.createElement("a");
                //console.log(res.data)
                docUrl.href = FILE;
                var file = filename.replace("/", " ")
                docUrl.download = file
                
                document.body.appendChild(docUrl);
                docUrl.click()
            })
        },
    }
}

</script>

<style>
.hit {
    border: 2px solid blue;
    margin-top: 10px;
    margin-bottom: 10px;
    margin-right: 10px;
    margin-left: 10px;
}

.btn-upload {
    width: 100%;
}

.btn {
    padding: 15px 26px;
}
.viewer {
    max-width: 800px;
    margin: auto;
    border: 15px solid green;
    background-color: white;
}
.artist {
    cursor: pointer;
    user-select: none;
}

.btn-list {
    display: inline-block;
    cursor: pointer;
    float: right;
}

ul {
    text-align: left;
}

.li-music {
    margin: 0 0 15px 0;
}
</style>
