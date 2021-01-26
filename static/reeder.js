async function getAllReadingPages() {
    let url = $(location).attr('href');

    res = await axios.get(`${url}/pages`)
    let pages = res.data.pages
    let arr = pages.sort(function(a, b) {
        return a.id - b.id;
      })
    printAllReedPages(arr)
    content(arr)
    viewCurrentPage()
    pageMark()
}

// Turn data from edtitorJS to html representation
function editorToText(content) {
    let html = ''
    content.blocks.map(obj => {

        switch (obj.type) {
            case 'paragraph':
                html += `<p>${obj.data.text}</p>`;
                
                break;
            case 'header':
                html += `<h${obj.data.level}>${obj.data.text}</h${obj.data.level}>`
                break;
        }
        
    })
    return html
}


// display html data from a page
function content(pages) {
    for(let page of pages){
        let data = JSON.parse(page.content)

        $('#caro-items').append(`
            <div id="${page.id}" class="hide text" >
                    ${editorToText(data)}
            </div>
        `)
    }
    
}
let page_index = 0




// show the  current page or first page
function viewCurrentPage(){
    
    let nextPage = $('#caro-items div').get(page_index)
    nextPage.classList.toggle('hide')
    page_index += 1
   
}

function pageMark(){

    let span = $('#page-container span')
    $('#caro-items div').each(function(index){
        if(!$(this).hasClass('hide')){
            console.log($(this).attr('id'))
            span[index].classList.add('badge-success')
            
        }else if($(this).hasClass('hide')){
            span[index].classList.remove('badge-success')
        }
    })
}


$('#next-slide').on('click', nextSlide)

function nextSlide(e){
    e.preventDefault()
    
    if(page_index > 0){
        let prevPage = $('#caro-items div').get(page_index-1)
        prevPage.classList.toggle('hide')
    }
    if($('#caro-items div').get(page_index) === undefined){
        $('#caro-items div').get(0).classList.toggle('hide')
        page_index = 0
    }else{
        $('#caro-items div').get(page_index).classList.toggle('hide')
    }
    page_index += 1
    pageMark()
}

$('#previos-slide').on('click', previosSlide)

function previosSlide(e){
    e.preventDefault()
    
    if((page_index-1) <= 0){
        return
    }else{
        page_index -= 1
        $('#caro-items div').get(page_index-1).classList.toggle('hide')
        $('#caro-items div').get(page_index).classList.toggle('hide')
    }
    pageMark()
}

function printAllReedPages(pages) {
    // itterate over the pages we get from the server
    for(let page of pages){
        // check if page content is null so it dos not break ower functions
        if(!page.content){
            page.content = 'Empty'
            
        }else{
            
            $('#page-container').append(`
            <div class="col-md-1 m-2">
                <div class="" >
                <span id='${page.id}' class="badge badge-secondary ">${page.page_title}</span>
                    
                </div>
            </div>
            
        `)
        }
    }
    
}

$(document).ready(getAllReadingPages())


