<template>
    <div class="editor" v-if="data != undefined">
        <div v-if="data.length > 1">
            <label>Artist: </label> <input type="text" v-model="data[0].artist"/><br>
            <label>Album: </label> <input type="text" v-model="data[0].album"/>
        </div>
        <div v-if="data.length != 1">
            <ul>
                <div v-for="song in data" :key="song.title">
                    <li>
                        <label>Title:</label> <input type="text" v-model="song.title"/> 
                        <label>Track:</label> <input type="text" v-model="song.track"/><br>
                    </li>
                </div>
            </ul>
        </div>
        <div v-else>
            <label>Title:</label> <input type="text" v-model="data[0].title"/><br>
            <label>Artist:</label> <input  type="text" v-model="data[0].artist"/><br>
            <label>Album:</label> <input type="text" v-model="data[0].album"/><br>
            <label>Track:</label> <input type="text" v-model="data[0].track"/><br>
        </div>
        <button class='btn btn-default' @click="$emit('cancel-edit')">Cancel</button> <button class='btn btn-default' @click="save()">Save</button>
    </div>
</template>

<script>

import axios from "axios";

export default {
    props: {
        info: {
            artist: String,
            title: String,
            track: Number,
            album: String
        },
        id: String,
        library: Boolean
    },

    data() {
        return {    
            data: this.info,
        };
       
    },

    methods: {
        save() {
            
            
          if(this.library) {
            const path = "http://192.168.0.16:5000/api/library/edit" 
            axios.post(path, {"data": this.info[0]})
            this.$emit('saved-edit')
          } else {
            const path = "http://192.168.0.16:5000/api/download/add";

            if (this.data.length > 1) {
                for(var i = 1; i < this.data.length; i++) {
                    this.data[i]["album"] = this.data[0].album
                    this.data[i]["artist"] = this.data[0].artist
                }
            }

            const response = axios.post(path, {
                    "data": this.data, 
                    "id": this.id, 
                    "overwrite": false, 
                    "new": true}
                    )
            if (response.data.success) {
                this.$emit('saved-edit')
            } else {
                alert("Failed to save the song/songs because one already exists")
            }
          }
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
.btn {
    padding: 15px 26px;
}

input {
    float: right;
    width: 100%;
}

.editor {
    border: 2px solid blue;
    max-width: 250px;
}

.editor button {
    pla: right;
}

</style>