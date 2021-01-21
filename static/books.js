
$('#all-books').on('click', getAllBooks);

$('#my-books').on('click', getMyBooks);

async function getAllBooks(e){
    if (e){
        e.preventDefault(); 
    }
    $('#books').html('')

    res = await axios.get('/api/books');
    list = res.data.books;
    this.user = res.data.user
    listBooks(list)
}

async function getMyBooks(e){
    e.preventDefault(); 
    $('#books').html('')

    res = await axios.get('/api/books');

    list = res.data.books;
    userId = res.data.user

    listBooks(list, userId)  
}


function listBooks(books, userId) {
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

function bookCard(book, userId){
    
    $('#books').append(`
    <div class="col-auto">
    <div class="card m-1" style="width: 18rem;">
        <img class="card-img-top" src="${book.cover}" alt="Card image cap">
        <div id="${book.id}" class="card-body">
          <h5 class="card-title">${book.title}</h5>
          <p class="card-text">${book.description}</p>
          <a href="book/${book.id}/read" class="btn btn-success m-1">Read Book</a>
        </div>
      </div>
    </div>
    `)
}

getAllBooks()