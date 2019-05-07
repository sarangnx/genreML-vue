<template>
    <div id="content">
        <div id="wrapper">
            <mode></mode>
        </div>
        <footer class="page-footer">
            <div class="status-bar">

            </div>
            <div class="toggle-button">
                <div class="switch" id="toggle">
                    <label>
                        SINGLE
                        <input type="checkbox" onclick="toggle(this)">
                        <span class="lever"></span>
                        BATCH
                    </label>
                </div>
            </div>
        </footer>
    </div>
</template>

<script>
export default {
    name: 'landing-page',
}
</script>

<style scoped>
#content{
    height: 100%;
}

#wrapper{
    height:90%;
}

.page-footer{
    padding: 0px;
    height:10%;
    display: flex;
    background: #000000;
}

.toggle-button{
    width: 20%;
    height: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
}

.status-bar{
    width: 80%;
    height: 100%;
}

/* Change Toggle Button color */

.switch label .lever{
    background: #c78484;
}

.switch label .lever:after{
    background: #a62626;
}

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
/* Hide batch mode initially */
#batch-mode{
    display: none;
}
</style>
