<template>
    <div id="single-mode">
        <div class="title">
            <span>Choose a Song :</span>
        </div>

        <div class="selection-box">
            <button v-for="item in folders" v-bind:key="item.id" v-bind:title="item.name" @click="openFolder(item.path)">
                <i class="material-icons">folder</i>               
                <label>{{ item.name | trim(10) }}</label>
            </button>
            <button v-for="item in songs" v-bind:key="item.id" v-bind:title="item.title">
                <img v-if="item.picture[0]" v-bind:src="retimage(item.picture[0].data,item.picture[0].format)" />
                <v-icon v-else name="music"/>
                <label>{{ item.title | trim(10) }}</label>
            </button>
        </div>
        <div class="classify-button" @click="lol">
            <a class="waves-effect waves-light btn"><i class="material-icons right">play_arrow</i>CLASSIFY</a>
        </div>
    </div>
</template>

<script>
import { mapGetters } from 'vuex';
const { mapState } = require('vuex');
const { ipcRenderer } = require('electron');
const fs = require('fs');
const path = require('path');
const mm = require('musicmetadata');
const readChunk = require('read-chunk');
const fileType = require('file-type');

export default {
    name: 'single-mode',
    data: () => {
        return{
            foldersArray: null,
            songsArray: null,
            pwd: null,
        }   
    },
    computed:{
        ...mapGetters({
            musicpath: 'getPath'
        }),
        folders:{
            get:function(){
                return this.foldersArray;
            },
            set:function(data){
                this.foldersArray = data;
            }
        },
        songs: {
            get: function(){
                return this.songsArray;
            },
            set: function(data){
                this.songsArray = data;
            }
        }
    },
    methods: {
        lol(){
            console.log(this.musicpath);
        },
        refresh(musicpath){
            
            if(!musicpath){
                musicpath = this.pwd || this.musicpath;
            }

            let directory = [];
            let musicfiles = [];

            this.pwd = musicpath;

            fs.readdir(musicpath,(err, files) => {
                for( let file of files ){
                    let song = path.join(musicpath,file);

                    fs.stat(song,(err,stats) => {
                        //check if directory
                        if(stats.isDirectory()){
                            let meta = {
                                name: file,
                                path: song
                            }
                    
                            directory.push(meta);
                        } else {
                            /**
                             * look for mime type matching audio in the list.
                             * If audio/*
                             *  pull up the musicmetadata 
                             *  push it to array.
                             */
                            let buffer = readChunk.sync(song, 0, 4100);
                            let type = fileType(buffer);
                            let mime = type? type.mime : null ;
                            if(  /audio/.test(mime) ){
                                let readable = fs.createReadStream(song);
                                mm(readable, (err, metadata) => {
                                    metadata = { ...metadata, path:song };
                                    musicfiles.push(metadata);
                                });
                            }
                        }
                    });
                }
            });
            this.folders = directory;
            this.songs   = musicfiles;
        },
        back(){
            this.refresh(path.join(this.pwd,'..'));
        },
        retimage(base64,type){
            return `data:image/${type};base64,${base64.toString('base64')}`;
        },
        openFolder(folderPath){
            this.refresh(folderPath);
        }
    },
    filters:{
        trim: function(title,size){
            if (title.length > size)
                return title.slice(0,size) + "...";
            else
                return title;
        }
    }
}
</script>

<style scoped>
#single-mode,#batch-mode{
    height: 100%;
}

.selection-box{
    background: #404040;
    height: 80%;
    overflow-y: auto;
}

.title, .classify-button{
    height:10%;
}

.classify-button{
    display: flex;
    justify-content: flex-end;
    align-items: center;
}

.title{
    color:#c3c3c3;
    font-weight: bold;
    font-variant: petite-caps;
}

::-webkit-scrollbar {
    width: 5px;
}

::-webkit-scrollbar-thumb {
    background: #000000;
}

::-webkit-scrollbar-track {
    background: #9a9c9a;
}
</style>
