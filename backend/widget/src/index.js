import WaveSurfer from "wavesurfer.js";
import './style.css';

// Constants
const playSvg = 'http://127.0.0.1:8000/media/widget/play.svg'
const pauseSvg = "http://127.0.0.1:8000/media/pause.svg";
const stopSvg = "http://127.0.0.1:8000/media/stop.svg";
const azrecoLogoSvg = "http://127.0.0.1:8000/media/azreco_logo.svg";

// Current Browser URL
let currentUrl = window.location.href;
// Arguments
let dataToken = document.currentScript.getAttribute('data-token');
let dataSize = document.currentScript.getAttribute('data-size');
// create query for getting Audio stream
const queryUrl = `http://127.0.0.1:8000/api/v1/synthesis/audio/?link=${encodeURIComponent(currentUrl)}`;

// Containers
let playerContainer;
let playPauseButton;
let stopButton;
let logoContainer;

// Images
let playPauseImage;
let stopImage;
let logoImage;
let azrecoLink;

// create WaveForm container
let waveform = document.createElement('div');
waveform.setAttribute("id", "waveform");
waveform.style.display = "none";
document.body.appendChild(waveform);

// create WaveSurfer
let wavesurfer = WaveSurfer.create({container: '#waveform'});

// Show or Hide Player Container
const makeVisible = (isVisible) => {
    if (isVisible) {
        playerContainer.style.display = "flex";
    } else {
        playerContainer.style.display = "none";
    }
};


// Create and init HTML elements
const initElements = () => {
    // div
    playerContainer = document.createElement("div");
    playerContainer.className = "azreco-player-container";
    playPauseButton = document.createElement("div");
    playPauseButton.className = "azreco-play-pause-button";
    stopButton = document.createElement("div");
    stopButton.className = "azreco-stop-button";
    // img
    playPauseImage = document.createElement("img");
    playPauseImage.className = "azreco-play-pause-image";
    playPauseImage.src = playSvg;
    stopImage = document.createElement("img");
    stopImage.className = "azreco-stop-image";
    stopImage.src = stopSvg;
    logoImage = document.createElement("img");
    logoImage.className = "azreco-logo-image";
    logoImage.src = azrecoLogoSvg;
    // a
    logoContainer = document.createElement("a");
    logoContainer.className = "azreco-logo-container";
    logoContainer.href = "https://azreco.az/";

    playPauseButton.appendChild(playPauseImage);
    stopButton.appendChild(stopImage);
    logoContainer.appendChild(logoImage);
    // append to main container
    playerContainer.appendChild(playPauseButton);
    playerContainer.appendChild(stopButton);
    playerContainer.appendChild(logoContainer);
    // append to body
    document.body.appendChild(playerContainer);
};

const getBufferData = async () => {
    const response = await fetch(queryUrl);
    if (!response.ok) {
        throw new Error('Cant get Audio File, Server Error');
    }
    return await response.arrayBuffer();
};

const setupWaveSurfer = async (buffer) => {
    let audioCtx = new AudioContext();
    // Decode buffer
    let decodedData = await audioCtx.decodeAudioData(buffer);
    // Load to WaveSurfer
    wavesurfer.loadDecodedBuffer(decodedData);
};

// Click Listeners
playPauseButton.onclick = () => {
    wavesurfer.playPause();
};

stopButton.onclick = () => {
    wavesurfer.stop();
};

// WaveSurfer Event Listeners
wavesurfer.on('ready', function () {
    makeVisible(true);
});

wavesurfer.on('play', function () {
    playPauseImage.src = pauseSvg;
});

wavesurfer.on('pause', function () {
    playPauseImage.src = playSvg;
});

wavesurfer.on('finish', function () {
    console.log('finish');
});


// Main Function
const start = async () => {
    try {
        initElements();
        const buffer = await getBufferData();
        await setupWaveSurfer();
    } catch (error) {
        console.log(error.message);
    }
};


start();
