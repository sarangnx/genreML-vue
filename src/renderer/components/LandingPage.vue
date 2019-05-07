<template>
    <div id="content">
        <div id="wrapper">
            <single-mode></single-mode>
            <!-- <batch-mode></batch-mode> -->
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
    components:{
        SingleMode: require('./LandingPage/single-mode').default
    },
    methods :{

    }
}
</script>

<style scoped>
#content{
    height: 100%;
}

#wrapper{
    height:90%;
    padding: 20px;
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

</style>
