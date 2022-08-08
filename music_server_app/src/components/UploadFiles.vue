<template>
    <div id="UploadFiles">

        <label>File:
            <input type="file" ref="fileInput" accept="music/*,.m4a" @change="handleFileUpload($event)"/>
        </label>

        <button class="btn btn-default" @click="submitFile()"> Upload </button>

    </div>
</template>

<script>
import axios from 'axios';


export default {
    components: {
        
    },

    data() {
        return {
            file: null
        };
       
    },

    methods: {
        /**
         * Uploads file to server.
         * @param {Event} event The form change event with the file to be uploaded.
         */
        handleFileUpload(event) {
            this.file = event.target.files[0];
        },
        /**
         * Uploads the file to server.
         */
        submitFile() {
            if (this.file == null) {
                return;
            }

            let formData = new FormData();
            formData.append('file', this.file)

            const path = this.window.location.origin + "/api/library/upload"
            axios.post(path, formData, {
                'Content-Type': 'multipart/form-data'
                })
                .then (responce => {
                    this.$refs.fileInput.value = "";
                    console.log(responce)
                })

            this.$emit("done")
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
.viewer {
    max-width: 800px;
    margin: auto;
    border: 15px solid green;
}
.artist {
    cursor: pointer;
    user-select: none;
}

ul {
    text-align: left;
}
</style>
