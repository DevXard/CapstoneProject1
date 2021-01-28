$('#add-page').on('click', createPage);

async function createPage(e){
    e.preventDefault();
    let title = $('#page-title').val();
    let url =$(location).attr('href');
    res = await axios.post(`${url}/add-page`, {title: title})

    $('#page-container').html('')
    getAllPages()
}

async function getAllPages() {
    let url = $(location).attr('href');

    res = await axios.get(`${url}/get-pages`)
    let pages = res.data.pages
    printAllPages(pages)
}

function printAllPages(pages) {
    // itterate over the pages we get from the server
    for(let page of pages){
        // check if page content is null so it dos not break ower functions
        if(!page.content){
            page.content = 'Empty'
        }else{
            // parse all pages with content not eaqual to null
            let data = JSON.parse(page.content)
            // use createText from editor.js to translate json data into readable text
            $('#page-container').append(`
            <div class="col-md-3 mb-2">
                <div id="page-card" class="card" >
                    <div class="card-body">
                    <h5 class="card-title">${page.page_title}</h5>
                    <p id='card-content' class="card-text overflow-auto">${createText(data.blocks)}</p>
                    </div>
                    <a href="/pages/${page.id}" class="btn btn-success">Go to Page</a>
                </div>
            </div>
            
        `)
        }
    }
    
}

getAllPages()