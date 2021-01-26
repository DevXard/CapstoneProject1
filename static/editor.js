
// Save a new version of the page
$('#save-page').on('click', savePageContent);

async function savePageContent(e) {
    e.preventDefault();
    let url = $(location).attr('href');
    editor.save().then( async(outputData) => {
        res = await axios.post(`${url}/save-page`, outputData)
        console.log(res)
    })
}

// Request all versions of the current page and list them
$('#all-versions').on('click', getPagesVersion);

async function getPagesVersion(e){
    e.preventDefault();
    uiExpand()
    let url = $(location).attr('href');
    res = await axios.get(`${url}/versions`)
    console.log(res)
    listVersions(res.data.vers)
}

// DELETE BUTTON
$('#versions-display').on('click', '.btn-danger', deletePage);

async function deletePage(e){
    e.preventDefault();
    let url = $(location).attr('href');
    let urlEnd = $(this).attr('data-version-tId')
    // console.log($(this).attr('data-version-tId'))
    res = await axios.delete(`${url}/delete/${urlEnd}`)
    
    $('#versions-display').html('')
    listVersions(res.data.vers)
}

// REVERT BUTTON
$('#versions-display').on('click', '.btn-success', RevertToPage);

async function RevertToPage(e){
    e.preventDefault();
    let url = $(location).attr('href');
    let urlEnd = $(this).attr('data-version-tId')
    console.log(urlEnd)
    res = await axios.post(`${url}/revert/${urlEnd}`)

    $('#versions-display').html('')
    listVersions(res.data.vers)

    $('#editorjs').html('')
    getPageData()
}

// DELETE PAGE AND ALL VERSIONS
$('#page-and-ver-del').on('click', deletePageAndVer);

async function deletePageAndVer(e){
    e.preventDefault();
    let url = $(location).attr('href');
    res = await axios.delete(`${url}/delete`)
    window.location.href='http://127.0.0.1:5000/books'
}

// List all versions of the page
function listVersions(arr) {
    let url = $(location).attr('href');
    for(let version of arr) {
        let data = JSON.parse(version.content)
        
        
        $('#versions-display').append(`
            <div class="col-md-4 mb-2">
                <div class="card" style="width: 13rem; height: 20rem ">
                    <div class="card-body m-1">
                        <h5 class="card-title"></h5>
                        <div class="">
                            <p id="version-card-content" class="card-text overflow-auto">
                                ${createText(data.blocks)}
                            </p>
                        </div>
                    </div>
                    <div id='delete-revert' class="delete-revert container-fluid m-1">
                    <a data-version-tId="${version.transaction_id}" class="btn btn-sm btn-success">Revert</a>
                    <a data-version-tId="${version.transaction_id}"  class="btn btn-sm btn-danger">Delete</a>
                    </div>
                </div>
            </div>
        `)
    }
}
// href="${url}/delete/${version.transaction_id}"

// Transform theJson from editorjs to normal text
function createText(arr){
    let result = ''
    for (let text of arr){
        result += text.data.text + '\n'
    }
    
    return result
}


// Expand the UI on the left to vew all versions of the Page And create a button to go back
function uiExpand() {
    $('.fig1').toggleClass('widen')
    $('#shrink').toggleClass('hide')
    $('#all-versions').toggleClass('hide')
    $('#back-button').toggleClass('hide')
}

// Return UI to original state
$('#back-button').on('click', resetUI)

function resetUI(e) {
    e.preventDefault()
    $('#versions-display').html('')
    $('.fig1').toggleClass('widen', 10000)
    $('#shrink').toggleClass('hide',10000)
    $('#all-versions').toggleClass('hide')
    $('#back-button').toggleClass('hide')
}

//  Request the page Content from the server and add it to the eddiotor
async function getPageData() {
    let url = $(location).attr('href');
    res = await axios.get(`${url}/all-pages`)
    let data = JSON.parse(res.data.page.content)
  
    // return editor with the data loaded from ower database
    return editor = new EditorJS({
        /**
         * Id of Element that should contain Editor instance
         */
        holder: 'editorjs',
      
        tools: { 
          header: {
            class: Header, 
            inlineToolbar: ['link'] 
          }, 
          list: { 
            class: List, 
            inlineToolbar: [
                  'link',
                  'bold'
            ]
          }, 
          quote: { 
              class:Quote, 
              inlineToolbar: true
          }
        }, 
        data:data
      });
}

$(document).ready(getPageData()) 