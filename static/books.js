
$('#all-books').on('click', getAllBooks);

$('#my-books').on('click', getMyBooks);

$('#books').on("click", 'a', async function() {
    let bookId = $(this).data('book-id') 
    res = await axios.post(`/add-remove-like/${bookId}`)
  });

async function getAllBooks(e){
    if (e){
        e.preventDefault(); 
    }
    $('#books').html('')

    res = await axios.get('/api/books');
    console.log(res.data.likes)
    list = res.data.books;
    this.user = res.data.user
    listBooks(list)
    likes(res.data.likes, list)
    
}

async function getMyBooks(e){
    e.preventDefault(); 
    $('#books').html('')

    res = await axios.get('/api/books');
    let bookLikes = await axios.get('/api/books');
    let like = bookLikes.data.likes

    list = res.data.books;
    userId = res.data.user

    listBooks(list, userId)  
    likes(like, list)
}

$('#books').on('click','.fa-star', function(){
    $(this).toggleClass('liked')
})

function likes(likes, books){
    if(!Array.isArray(books))return
    for(let i = 0; i < likes.length; i++){
        if(likes[i].user_id === this.user){
            $( `#${books[i].id}`).find(`
                .fa-star
            `).addClass('liked')
        }
    }
}

function listBooks(books, userId) {
    if(!Array.isArray(books))return
    for(let book of books){
        if(userId){
            if(userId == book.user_id){
                bookCard(book)
                $(`#${book.id}`).append(`
                <a href="book/${book.id}/write" class="btn btn-primary m-1">Write</a>
                `)
            }
        }else{
            bookCard(book)
            
            if(this.user === book.user_id){
                $(`#${book.id}`).append(`
                <a href="book/${book.id}/write" class="btn btn-primary m-1">Write</a>
                `)
            }
        }
    }
}

$('#Search').on('click', searchBook);

async function searchBook(e){
    e.preventDefault()
    $('#books').html('')
    let search = $('#search-input').val()
    let res = await axios.get(`/api/search`, {params:{term: `${search}`}})
    let bookLikes = await axios.get('/api/books');
    let like = bookLikes.data.likes
    let list = res.data.books
    
    listBooks(list)
    likes(like, list)
}



function bookCard(book, userId){
    
    $('#books').append(`
    <div class="col-auto">
    <div class="card m-1" style="width: 18rem;">
        <img class="card-img-top" src="${book.cover}" alt="Card image cap">
        <div id="${book.id}" class="card-body">
            <div class="d-flex justify-content-between">
                <h5 class="card-title">${book.title} </h5>
                <a data-book-id="${book.id}" ><i class="fas fa-star"></i></i></a>
            </div>
          <p class="card-text">${book.description}</p>
          <a href="book/${book.id}/read" class="btn btn-success m-1">Read Book</a>
        </div>
      </div>
    </div>
    `)
}



getAllBooks()