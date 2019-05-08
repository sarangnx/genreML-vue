<template>
    <div id="single-mode">
        <div class="title">
            <span>Choose a Song :</span>
        </div>

        <div class="selection-box">
            <div class="navigation-area">
                <div>
                    <button @click="back" title="Back"><i class="material-icons">arrow_back</i></button>
                    <button @click="refresh(pwd)" title="Back"><i class="material-icons">refresh</i></button>
                </div>
            </div>

            <div class="display-area">
                <button v-for="item in folders" 
                        v-bind:key="item.id" 
                        v-bind:title="item.name" 
                        @click="openFolder(item.path)">
                    <i class="material-icons">folder</i>
                    <label>{{ item.name | trim(10) }}</label>
                </button>
                <button v-for="item in songs" 
                        v-bind:key="item.id"
                        v-bind:title="item.title || item.filename"
                        @click.self="toggleSelect($event)"
                        v-bind:data-path="item.path">
                    <img v-if="item.picture[0]" v-bind:src="retimage(item.picture[0].data,item.picture[0].format)" />
                    <i class="material-icons" v-else>music_note</i>
                    <label>{{ item.title | trim(10) }}</label>
                </button>
            </div>
        </div>
        <div class="classify-button" >
            <div id="output">

            </div>
            <button class="waves-effect waves-light btn"  @click="classify"><i class="material-icons right">play_arrow</i>CLASSIFY</button>
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

const {PythonShell} = require('python-shell');

export default {
    name: 'single-mode',
    data: () => {
        return{
            foldersArray: null,
            songsArray: null,
            pwd: null,
            selectedList: null
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
        },
        selected: {
            get: function(){
                return this.selectedList;
            },
            set: function(el){
                this.selectedList = el;
            }
        }
    },
    methods: {
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
                                    metadata = { ...metadata, path:song, filename: file };
                                    musicfiles.push(metadata);
                                    readable.close();
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
        },
        toggleSelect(event){
            let element = event.target;
            
            if(!this.selected){
                element.classList.add("selected");
                this.selected = element;
            } else {
                let el = this.selected;
                if(el === element){
                    el.classList.remove("selected");
                    this.selected = null;
                } else {
                    el.classList.remove("selected");
                    element.classList.add("selected");
                    this.selected = element;
                }
                
            }
        },
        classify(){
            if(!this.selected){
                return;
            }

            let el = this.selected;
            let datapath = el.getAttribute('data-path');

            let options = {
                args: [datapath]
            }
            let script = path.join(__dirname,"../../../","predictor",'test.py');
            let shell = new PythonShell(script,options);

            let output = document.getElementById('output');

            shell.on('message', (message) => {
                output.innerHTML = message;
            })

        }
    },
    beforeMount(){
        this.refresh(this.musicpath);
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
.navigation-area{
    height: 10%;
}

.display-area{
    height: 90%;
    padding:10px;
}

/**  ==========================================================
 *   .navigation-area : back and refresh buttons etc..
 *   .display-area    : song cover images, folder buttons etc..
 *   ==========================================================
 */
.navigation-area{
    display: flex;
    justify-content: space-between;
    flex-direction: row;
}

.navigation-area button{
    height: 40px;
    width: 40px;
    background:none;
    border:none;
    outline:none;
    padding:0px;
}

.navigation-area button:hover, 
.display-area button:hover{
    background: rgba(183, 183, 183, 0.5);
    box-shadow: 0px 0px 3px 0px black;
}

.navigation-area button:active,
.display-area button:active{
    background: rgba(183, 183, 183, 0.3);
    box-shadow: 0px 0px 3px 0px inset;
}

.navigation-area button > .material-icons{
    width:40px;
    height:40px;
    padding: 5px;
    font-size: 30px;
}

.display-area button > .material-icons{
    font-size: 70px;
}

.navigation-area button:active > .material-icons {
    transform: translateY(1px);
}

.display-area label{
    font-size: 15px;
    color: rgb(255, 255, 255);
    text-shadow: 1px 1px 1px black;
}

.display-area button{
    border: none;
    background: none;
    outline:none;
    padding: 0px;
    display: flex;
}

.display-area button{
    flex-direction: column;
    align-items: center;
    justify-content: center;
    border-radius: 10px;
    height: 100px;
    width: 100px;
    margin: 10px;
}

.display-area{
    display: flex;
    flex-wrap: wrap;
    flex-direction: row;
    overflow-x: hidden;
    overflow-y: auto;
    padding: 10px;
    max-height: 80%;
    max-width: 99%;
}

#selection-view-grid button .material-icons {
    height: 70px;
    width: 70px;
}

.display-area button img{
    width: 70px;
    height: 70px;
}

/* This stops child elements from propagating events */
button > * {
  pointer-events: none;
}

.selected{
    background: #232323!important;
}

#output{
    width:80%;
    height:100%;
    display: flex;
    align-items: center;
    color:white;
}
</style>
