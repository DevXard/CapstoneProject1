$('#brouse-movies').on('click', moviesData)


async function moviesData(e){
    e.preventDefault()
    uiExpand()
    let data = $('#movie-search').val()
    res = await axios.get('/api/movies', {params: {query: data}})
    console.log(res)
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