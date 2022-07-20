<template>

<div id="YoutubeDownloader">

    <div class="viewer">
        <div id="searchbar">
            <input id="search" v-model="queue.queue" type="text" placeholder="Search...">
            <button class='btn btn-search' @click="search()"> <i class="fa fa-search"/> </button>
        </div>
        <div id="downloaded">
            <div v-for="download in downloaded" :key="download.name">
                <label>{{download.name}}</label><button class="btn btn-default" @click="download.show=true">Save</button>
                <Editor :info="download.data" :id="download.id" @cancel-edit="download.show=false" @saved-edit="get_downloaded()" v-show="download.show"/>        
            </div>
        </div>
        <div id="failed">
            <div v-for="download in failed" :key="download.name">
                <label>{{download.name}}</label><button class="btn btn-default" @click="retry(download.id)">Retry</button><button class="btn btn-default">Cancel</button>      
            </div>
        </div>
        <div id="result">
            <div class="hit" v-for="hit in search_results.data" :key="hit.title">
                <h1>{{hit.title}}</h1>
                <h2>Duration: {{hit.duration}}</h2>
                <p>Type: {{hit.type}}</p> 
                <p>Url: <a href="hit.url">{{hit.url}}</a></p>
                <button class="btn btn-default btn-download" @click="download(hit.type, hit.url, hit.title)">Download</button>
            </div>
        </div>
        
    </div>
</div>
</template>

<script>
import axios from 'axios';
import Editor from "@/components/TagEditor.vue";

export default {
    components: {
        Editor
    },

    data() {
        return {
            queue: {
                queue: "",
                limit: 10
            },
            search_results: {},
            downloaded: [],
            failed: [],
    
        };
       
    },

    async created() {
        this.get_downloaded()
        //this.timer = setInterval(this.get_downloaded, 5000);

    },

    methods: {
        async get_downloaded() {
            const path = "http://192.168.0.16:5000/api/download/downloaded";

            var response = await axios.get(path, {});

            response = response.data
            for (var i = 0; i < response.data.length; i++) {
                response.data[i]["show"] = false
            }
            this.downloaded = response.data

            this.failed = response.failed
        },

        async search() {
            const path = "http://192.168.0.16:5000/api/youtube/search";

            const responce = await axios.post(path, {
                queue: this.queue.queue, 
                limit: this.queue.limit
                });
            this.search_results = responce.data;
        },

        async retry(id) {

            const path = "http://192.168.0.16:5000/api/download/retry"

            axios.post(path, {"id": id})
        },

        async download(type, url, title) {
            const path = "http://192.168.0.16:5000/api/youtube/download";
            axios.post(path, {
                type: type,
                url: url,
                title: title
            })
        }
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

.btn {
    padding: 15px 26px;
   
}

.searchbar {
    display: table;
}

.viewer {
    max-width: 800px;
    margin: auto;
    border: 15px solid green;
}

.btn-download {
    width: 100%;
    background-color: lightblue;
}

.viewer input[type=text] {
    padding: 5px;
    width: 90%;
    font-size: 17px;
    float: left;
    margin: 0px;
}

.btn-search {
    width: 10%;
}

</style>