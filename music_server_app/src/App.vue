<template>
 <div id="app">
    <head>
        <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous" />
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <title>Music</title>
    </head>

    <nav>
      <a href="/library">Library</a>
      <a class="notification" href="/youtube"> Youtube Downloader 
        <span id="download_status" class="badgeleft">{{download_status.running}}</span>
        <span id="donwload_done" class="badgeright">{{download_status.done + download_status.failed}}</span>
      </a>

    </nav>
    <router-view> </router-view>
</div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      library_class: this.$route.path === "/" ? "active" : "",
      youtube_downloader_class: this.$route.path === "youtube" ? "active" : "",
      download_status: {
          running: 0, 
          done: 0,
          failed: 0
      },
    };
  },
  created() {
    this.timer = setInterval(this.get_download_status, 5000);
    this.get_download_status()
    console.log(window.location.origin)
  },
  methods: {
    async get_download_status() {
        const path = this.window.location.origin +  "/api/download/status";
        const responce = await axios.get(path, {})

        this.download_status = responce.data
    }
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 20px;
}

.notification {
    text-decoration: none;
    padding: 15px 26px;
    position: relative;
    display: inline-block;
    border-radius: 1px;
}

.notification .badgeright {
    position: absolute;
    top: -3px;
    padding: 2px 8px;
    border-radius: 50%;
    background: blue;
    color: white;
}

.notification .badgeleft {
    position: absolute;
    top: -3px;
    left: 3px;
    padding: 2px 8px;
    border-radius: 50%;
    background: red;
    color: white;
}

nav {
  background: green;
}

nav a {
  color: yellow;
}

body  {
  background-color: darkolivegreen;
}


</style>
