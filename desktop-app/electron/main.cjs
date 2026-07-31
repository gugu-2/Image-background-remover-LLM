const { app, BrowserWindow } = require('electron');
const path = require('path');
const { spawn } = require('child_process');
const http = require('http');

let mainWindow;
let backendProcess;
const isDev = !app.isPackaged;
const port = 8000;

function startBackend() {
  console.log("Starting backend...");
  if (isDev) {
    // In dev, run the python script from the venv
    const pythonExecutable = path.join(__dirname, '../../venv/Scripts/python.exe');
    // Using the uvicorn command since it's easier to run
    backendProcess = spawn(pythonExecutable, ['-m', 'uvicorn', 'bg_remover.api:app', '--host', '127.0.0.1', '--port', '8000'], {
      cwd: path.join(__dirname, '../../'),
      detached: false,
      stdio: 'pipe'
    });
  } else {
    // In production, run the compiled exe
    const exePath = path.join(process.resourcesPath, 'backend', 'backend.exe');
    console.log("Starting production backend at: " + exePath);
    backendProcess = spawn(exePath, [], {
      cwd: path.join(process.resourcesPath, 'backend'),
      detached: false,
      stdio: 'pipe'
    });
  }
  
  if (backendProcess && backendProcess.stdout) {
    backendProcess.stdout.on('data', (data) => console.log(`[API]: ${data}`));
    backendProcess.stderr.on('data', (data) => console.error(`[API ERROR]: ${data}`));
  }
}

function stopBackend() {
  if (backendProcess) {
    backendProcess.kill();
  }
}

function checkBackendReady(callback) {
  const req = http.get(`http://127.0.0.1:${port}/docs`, (res) => {
    callback();
  }).on('error', () => {
    setTimeout(() => checkBackendReady(callback), 500);
  });
}

function createWindow() {
  mainWindow = new BrowserWindow({
    width: 1200,
    height: 800,
    titleBarStyle: 'hidden',
    titleBarOverlay: {
      color: '#1a1a1a',
      symbolColor: '#ffffff'
    },
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false
    }
  });

  if (isDev) {
    mainWindow.loadURL('http://localhost:5173');
    mainWindow.webContents.openDevTools();
  } else {
    mainWindow.loadFile(path.join(__dirname, '../dist/index.html'));
  }

  mainWindow.on('closed', () => {
    mainWindow = null;
  });
}

app.whenReady().then(() => {
  startBackend();
  // Wait a bit for backend to start, then create window
  checkBackendReady(() => {
    createWindow();
  });

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createWindow();
    }
  });
});

app.on('window-all-closed', () => {
  stopBackend();
  if (process.platform !== 'darwin') {
    app.quit();
  }
});
