$('#brouse-movies').on('click', moviesData);
$('#search-lyrics').on('click', songLyrics);

async function songLyrics(e){
    e.preventDefault();
    uiExpand()
    let artist = $('#song-artist').val();
    let title = $('#song-title').val();
    let res = await axios.get('/api/song_lirycs', {params: {artist: artist, title:title}})
    let lyric = res.data.data.lyrics

    displayLyrics(lyric)
}

function displayLyrics(lyrics){
    $('#versions-display').append(`
    <div class="card overflow-auto m-2" style="width: 40rem; height: 20rem; left:3rem;">
        <div class="card-body m-1">
            <div class="">
                <p class=" center">${lyrics}</p>
                </div>
            </div>
        </div>
    `)
}

async function moviesData(e){
    e.preventDefault()
    uiExpand()
    let data = $('#movie-search').val()
    let res = await axios.get('/api/movies', {params: {query: data}})
    
    displayMovieDetails(res.data.data.info)
    displayMovieDetails(res.data.data.results)
}

function displayMovieDetails(movies){
    for(let movie of movies){
        $('#versions-display').append(`
            <div class="class="col-md-12 mb-2"">
                <div class="card overflow-auto m-2" style="width: 40rem; height: 10rem ">
                    <div class="card-body m-1">
                        <h3 class="card-title">${movie.Name}</h3>
                        <div class="">
                            <p  class="card-text ">${movie.wTeaser}</p>
                        </div>
                    </div>
                </div>
            </div>
        `)
    }
}