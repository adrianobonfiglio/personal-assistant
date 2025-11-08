const { app, BrowserWindow } = require('electron')

let mainWin;

const createWindow = () => {
  mainWin = new BrowserWindow({
    width: 1024,
    height: 600
  })
  load_home()
}

app.whenReady().then(() => {
  createWindow()
})

if (process.defaultApp) {
    if (process.argv.length >= 2) {
        app.setAsDefaultProtocolClient('assistant', process.execPath, [
            '--squirrel-uninstall',
        ]);
    }
} else {
    app.setAsDefaultProtocolClient('assistant');
}

app.on('open-url', (event, url) => {
    event.preventDefault();
    // Handle the URL here, e.g., open a specific page in your Electron app
    console.log(`Received URL: ${url}`);
    if(url === 'assistant://second'){
        load_second_page()
    }else if(url === 'assistant://home'){
        load_home()
    }else if(url === 'assistant://loader') {
        load_loader_page()
    }else if(url.startsWith('assistant://youtube-music')){
        open_youtube_music(url.replace('assistant://youtube-music/param=',''))
    }
});

// Handle protocol links when the app is launched via a protocol link
app.on('second-instance', (event, commandLine, workingDirectory) => {
    // Someone tried to launch a second instance with a protocol link
    const url = commandLine.find(arg => arg.startsWith('assistant://'))
    if (url) {
    console.log(`Received URL from second instance: ${url}`);
    // Process the URL in the existing instance
    }
});

const load_second_page = ()=>{ 
    mainWin.loadFile('second.html')
}

const load_home = ()=>{
    mainWin.loadFile('index.html')
}

const load_loader_page = ()=>{
    mainWin.loadFile('loader.html')
}

const open_youtube_music = (music)=>{
    mainWin.loadURL('https://music.youtube.com/search?q='+decodeURI(music));
    mainWin.webContents.on('did-finish-load', async () => {
      const result = await mainWin.webContents.executeJavaScript(
        "document.querySelector('.details-container button.yt-spec-button-shape-next').click();"
        +" document.querySelector('.ytmusic-player-bar').click();"
    );
      console.log('JavaScript executed, result:', result);
    });
}