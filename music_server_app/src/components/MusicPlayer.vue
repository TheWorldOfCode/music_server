<template>
<div id="MusicPlayer">
    <div>
        <audio style="display:none" ref="player">
            <source :src="song" type="audio/mpeg"/>
        </audio>
        
    </div>
    <div>
        <!--<button v-show="previously != -1" class="btn btn-default" @click="playPreviously()"> Pre </button>-->
        <button v-show="!isPlaying" class="btn btn-default" @click="toggleAudio()"> Play </button>
        <button v-show="isPlaying" class="btn btn-default" @click="toggleAudio()"> Pause </button>
        <!--<button v-show="next != -1" class="btn btn-default" @click="playPreviously()"> Next </button>-->
    </div>

    <div id="progress-bar" class="flex-grow bg-white border border-blue-200">

        <div class="overlay-container relative w-full h-full">
            <input  v-model=playbackTime type="range" min="0" :max="audioDuration" class="slider w-full h-full" id="position" name="position"/> 
                <div v-show="!audioLoaded"
                     class="w-full absolute top-0 bottom-0 right-0 left-0 px-2 pointer-events-none"
                     style="color: #94bcec">
                    Loading please wait...
                </div>

                <div
                    v-show="audioLoaded"
                    class="flex w-full justify-between absolute top-0 bottom-0 right-0 left-0 px-2 pointer-events-none"
                    >

                    <span class="text-sm" style="color: #94bcec" v-html="elapsedTime()"> </span>

                    <span class="text-sm" style="color: #94bcec" v-html="totalTime()">  </span>

                </div>
        </div>
    </div>

</div>
</template>

<script>

export default {
    components: {
},

    data() {
        return {
            previously: -1,
            next: -1,
            song: "/music/test_song.m4a",
            isPlaying: false,
            audioDuration: 100,
            audioLoaded: false,
            playbackTime: 0,
        };
       
    },

    methods: {
        // Play the prevously song in the playlist
        playPreviously() {

        }, 
        // Play the next song in the playlist
        playNext() {

        },
    //Set the range slider max value equal to audio duration
        initSlider() {

            var audio = this.$refs.player;
            if (audio) {
                this.audioDuration = Math.round(audio.duration);
            }
        },
        //Convert audio current time from seconds to min:sec display
        convertTime(seconds){
            const format = val => `0${Math.floor(val)}`.slice(-2);
            // eslint-disable-next-line no-unused-vars
            var hours = seconds / 3600;
            var minutes = (seconds % 3600) / 60;
            return [minutes, seconds % 60].map(format).join(":");
        },
        //Show the total duration of audio file
        totalTime() {
            var audio = this.$refs.player;
            if (audio) {
                var seconds = audio.duration;
                return this.convertTime(seconds);
            } else {
                return '00:00';
            }
        },
        //Display the audio time elapsed so far
        elapsedTime() {
            var audio = this.$refs.player;
            if (audio) {
                var seconds = audio.currentTime;
                return this.convertTime(seconds);
            } else {
                return '00:00';
            }
        },
        //Playback listener function runs every 100ms while audio is playing
        // eslint-disable-next-line no-unused-vars
        playbackListener(e) {
            var audio = this.$refs.player;
            //Sync local 'playbackTime' var to audio.currentTime and update global state
            this.playbackTime = audio.currentTime;
            
            //console.log("update: " + audio.currentTime);
            //Add listeners for audio pause and audio end events
            audio.addEventListener("ended", this.endListener);
            audio.addEventListener("pause", this.pauseListener);
        },
        //Function to run when audio is paused by user
        pauseListener() {
            this.isPlaying = false;
            this.listenerActive = false;
            this.cleanupListeners();
        },
        //Function to run when audio play reaches the end of file
        endListener() {
            this.isPlaying = false;
            this.listenerActive = false;
            this.cleanupListeners();
        },
        //Remove listeners after audio play stops
        cleanupListeners() {
            var audio = this.$refs.player;
            audio.removeEventListener("timeupdate", this.playbackListener);
            audio.removeEventListener("ended", this.endListener);
            audio.removeEventListener("pause", this.pauseListener);
            //console.log("All cleaned up!");
        },
        toggleAudio() {
            var audio = this.$refs.player;
            //var audio = document.getElementById("audio-player");
            if (audio.paused) {
                audio.play();
                this.isPlaying = true;
            } else {
                audio.pause();
                this.isPlaying = false;
            }
        },
    },
    mounted: function() {

      // nextTick code will run only after the entire view has been rendered
      this.$nextTick(function() {
        
        var audio=this.$refs.player;
        //Wait for audio to load, then run initSlider() to get audio duration and set the max value of our slider 
        // "loademetadata" Event https://www.w3schools.com/tags/av_event_loadedmetadata.asp
        audio.addEventListener(
          "loadedmetadata",
          // eslint-disable-next-line no-unused-vars
          function(e) {
            this.initSlider();
          }.bind(this)
        );
        // "canplay" HTML Event lets us know audio is ready for play https://www.w3schools.com/tags/av_event_canplay.asp
        audio.addEventListener(
          "canplay",
          // eslint-disable-next-line no-unused-vars
          function(e) {
            this.audioLoaded=true;
          }.bind(this)
        );
        //Wait for audio to begin play, then start playback listener function
        this.$watch("isPlaying",function() {
          if(this.isPlaying) {
            var audio=this.$refs.player;
            this.initSlider();
            //console.log("Audio playback started.");
            //prevent starting multiple listeners at the same time
            if(!this.listenerActive) {
              this.listenerActive=true;
              //for a more consistent timeupdate, include freqtimeupdate.js and replace both instances of 'timeupdate' with 'freqtimeupdate'
              audio.addEventListener("timeupdate",this.playbackListener);
            }
          }
        });
        //Update current audio position when user drags progress slider
        this.$watch("playbackTime",function() {
            var diff=Math.abs(this.playbackTime-this.$refs.player.currentTime);
        
          //Throttle synchronization to prevent infinite loop between playback listener and this watcher
          if(diff>0.01) {
            this.$refs.player.currentTime=this.playbackTime;
          }
        });
      });
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
