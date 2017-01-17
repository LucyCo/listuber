let g_userTextBox;
let g_lastSearch;

docReady(function() {
	// 2. This code loads the IFrame Player API code asynchronously.
	var tag = document.createElement('script');

	tag.src = "https://www.youtube.com/iframe_api";
	var firstScriptTag = document.getElementsByTagName('script')[0];
	firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

	g_userTextBox = document.getElementById("listEditorTextArea");
	let id = getParameterByName('id');
	g_lastSearch = localStorage.lastSearch;
	let isRestored = false; 
	if (id) {
		isRestored = restoreFromLocalStorage(g_userTextBox, "list" + id);
	}

	if (!isRestored && g_lastSearch) {
		restoreFromLocalStorage(g_userTextBox, g_lastSearch);
	}

	var el = document.getElementById('songsUl');
	var sortable = Sortable.create(el);
});

function init() {
	gapi.client.setApiKey("AIzaSyDNZ_ZsV6ld5zp17uuKh_C-LYNw2psjQWs");
	gapi.client.load('youtube', 'v3', function(){ console.log("youtube loaded.");});
}

function saveToLocalStorage(text, searchStr) {
	if (!text) {
		console.warn("text is null");
		return;
	}
	if (!searchStr) {
		console.warn("searchStr is null");
		return;
	}

	localStorage[searchStr] = text;
}

function restoreFromLocalStorage(element, savedSearch) {
	if (!element) {
		console.warn("element is null");
		return;
	}
	if (!savedSearch) {
		console.warn("savedSearch is null");
		return;
	}

	if (localStorage[savedSearch]) {
		element.value = localStorage[savedSearch];
		return true;
	}
	return false;
}

function getParameterByName(name, url) {
	if (!url) url = window.location.href;
	name = name.replace(/[\[\]]/g, "\\$&");
	var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
	results = regex.exec(url);
	if (!results) return null;
	if (!results[2]) return '';
	return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function idGenerator() {
  // Math.random should be unique because of its seeding algorithm.
  // Convert it to base 36 (numbers + letters), and grab the first 9 characters
  // after the decimal.
  return '_' + Math.random().toString(36).substr(2, 9);
};

function textAreaInput() {
	var text = g_userTextBox.value;
	var currentId = idGenerator();
	g_lastSearch = "list" + currentId;
	localStorage.lastSearch = g_lastSearch;
	saveToLocalStorage(text, g_lastSearch);
	var songs = text.split("\n");

	//need to take care of cases where there's either ID or last search that's generated - do not give them a new id!

	for(var i = 0; i < songs.length; i++)
	{
		var pattern =  new RegExp("[0-9]+.[ ]*[a-z]*");
		var result = pattern.exec(songs[i]);
		if(result != null)
		{
			if(songs[i].indexOf(result[0]) == 0) 
			{	
				songs[i] = songs[i].substring(result[0].length, songs[i].length);
				songs[i] = songs[i].trim();
			}
		}

		if(songs[i] == "") 
		{
			songs.splice(i, 1);
			--i;
		}
	}

	if(songs.length == 0) 
	{
		return;
	}

	var playlistDiv = document.getElementById("playlist");
	var idTitle = document.createElement('div');
	idTitle.className = 'idTitle';
	idTitle.innerHTML = "List ID :" + currentId;
	playlistDiv.appendChild(idTitle);

	var songsUl = document.getElementById("songsUl");
	empty(songsUl);
	var temp;
	for (var i = 0; i < songs.length; i++) 
	{
		temp = createSongElement(songs[i], i);
		songsUl.appendChild(temp);
	}
	playlistDiv.appendChild(songsUl);

	viewPlaylist();
}

function empty(element) {
	while (element.firstChild) 
	{
		element.removeChild(element.firstChild);
	}
}

function createSongElement(song, index) {
	var temp = document.createElement('li');
	temp.className = 'results';
	temp.innerHTML = song;
	temp.id = "songElement" + index;
	temp.setAttribute("data-song-id", index);
	temp.onclick = function(){playVideo(this)};
	return temp;
}

function search(divElement) {
	var request = gapi.client.youtube.search.list({
		q: divElement.textContent,
		maxResults: 5,
		part: 'snippet'
	});

	request.execute(function(response) {
	  	//error check
	  	console.debug(response);
	  	let videoId = null;
	  	let title;
	  	let thumbnailUrl;
	  	for (var i = 0; i < response.items.length && videoId == null; i++) {
	  		videoId = response.items[i].id.videoId;
		  	title = response.items[i].snippet.title;
		  	thumbnailUrl = response.items[i].snippet.thumbnails.default.url;
	  	}
	  	if (videoId) {	  		
		  	document.title = title + "- ListTuber";
		  	divElement.setAttribute("data-video-id", videoId);
		  	loadVideo(divElement.getAttribute("data-video-id"));
	  	}
	  });
} 


var g_player;
function onYouTubeIframeAPIReady() {
	g_player = new YT.Player('playerDiv', {
		height: '390',
		width: '640',
		events: {
			'onStateChange': onPlayerStateChange
		}
	});
}

function nextVideo() {
	if (!g_shuffle) { //shuffle is off ==> move to the next song
		// var nextSongId = parseInt(g_currentSong.getAttribute("data-song-id")) + 1;
		// var nextSong = document.getElementById("songElement" + nextSongId);
		let nextSongDiv = g_currentSong.nextSibling;

		if (nextSongDiv != null) {
			playVideo(nextSongDiv);
		}
	}
	
};

function previousVideo() {
	// var previousSongId = parseInt(g_currentSong.getAttribute("data-song-id")) - 1;
	// var previousSong = document.getElementById("songElement" + previousSongId);
		let previousSongDiv = g_currentSong.previousElementSibling;
	if (previousSongDiv != null) {
		playVideo(previousSongDiv);
	}	
};

var g_repeat = false;
function repeat() {
	g_repeat = true;
};

var g_shuffle = false;
function shuffle() {
	g_shuffle = true;
};

function stopVideo() {
	g_player.stopVideo();
}

function loadVideo(videoId)
{
	g_player.loadVideoById(videoId, 0, "large");
}

var g_currentSong;
function playVideo(divElement)
{
	if(g_currentSong)
	{
		g_currentSong.style.color = "#333";
	}

	g_currentSong = divElement;
	divElement.style.color = "red";
	if (divElement.getAttribute("data-video-id") == null) {
		search(divElement);
	}
	else {
		loadVideo(divElement.getAttribute("data-video-id"));
	}
}

function onPlayerStateChange(event) {
	if (event.data == YT.PlayerState.ENDED) {
		nextVideo();
	}
}

function toggle_visibility(id) {
	var e = document.getElementById(id);
	if(e.style.display == 'block')
		e.style.display = 'none';
	else
		e.style.display = 'block';
}


function viewEditor()
{
	let playlist = document.getElementById("playlist");
	playlist.style.display = 'none';

	let editor = document.getElementById("editor");
	editor.style.display = 'block';
}


function viewPlaylist()
{
	let editor = document.getElementById("editor");
	editor.style.display = 'none';

	let playlist = document.getElementById("playlist");
	playlist.style.display = 'block';
}

