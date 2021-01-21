$('#add-page').on('click', createPage);

async function createPage(e){
    e.preventDefault();
    let title = $('#page-title').val();
    
    let url =$(location).attr('href');
    
    res = await axios.post(`${url}/add-page`, {title: title})
    console.log(res)
}