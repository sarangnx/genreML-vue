/**
 * This Store stores the music path
 */
const state = {
    musicpath: '~/Music'
};
  
/**
 * Mutations (changes the state)
 * ---------
 * setPath: @argument state contains the current state value
 *          @argument value new music path 
 * 
 * This Method changes the state value
 */
const mutations = {
    setPath(state,value){
        state.musicpath = value;    
    }
};    
/**
 * Getters (gets the state value)
 * -------
 * getPath: @returns {string} path 
 */

const getters = {
    getPath(state){
        return state.musicpath;
    }
}

const actions = {
    setPath(context, value){
        context.commit('setPath', value);
    }
}

export default {
    state,
    mutations,
    getters,
    actions
}