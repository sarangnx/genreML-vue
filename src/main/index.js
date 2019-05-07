import { app, BrowserWindow, ipcMain } from 'electron'

import store from '../renderer/store';

/**
 * Set `__static` path to static files in production
 * https://simulatedgreg.gitbooks.io/electron-vue/content/en/using-static-assets.html
 */
if (process.env.NODE_ENV !== 'development') {
  global.__static = require('path').join(__dirname, '/static').replace(/\\/g, '\\\\')
}

let mainWindow
const winURL = process.env.NODE_ENV === 'development'
  ? `http://localhost:9080`
  : `file://${__dirname}/index.html`

function createWindow () {
    /**
    * Initial window options
    */
    mainWindow = new BrowserWindow({
        width: 800,
        minWidth:800,
        height: 600,
        minHeight:600,
        center:true,
        title: 'genreML',
        autoHideMenuBar:true,
        show: false
    });

    mainWindow.loadURL(winURL);

    mainWindow.on('closed', () => {
        mainWindow = null
    });
}

let musicpath = app.getPath('music');

app.on('ready', () => {
    createWindow();
    mainWindow.on('ready-to-show',()=>{
        mainWindow.show();
        // mainWindow.webContents.send('musicpath',musicpath);
    });
    store.dispatch('setPath',musicpath);
});

app.on('window-all-closed', () => {
    app.quit();
});

ipcMain.on('musicpath', (event) => {
    event.sender.send('musicpath',musicpath);
})
