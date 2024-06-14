const { app, BrowserWindow } = require('electron');
const path = require('path');
const exec = require('child_process').exec;

function createWindow () {
    // Create the browser window
    const mainWindow = new BrowserWindow({
        width: 800,
        height: 600,
        webPreferences: {
            preload: path.join(__dirname, 'preload.js')
        }
    });

    mainWindow.loadURL('http://127.0.0.1:5000/auth/login');
}

const flaskProcess = exec('python run.py');

app.whenReady().then(() => {
    createWindow();

    app.on('activate', function () {
        if (BrowserWindow.getAllWindows().length === 0) createWindow();
    });
});

app.on('window-all-closed', function () {
    if (process.platform !== 'darwin') app.quit();
    flaskProcess.kill();
});
