
$('#all-books').on('click', getAllBooks);

$('#my-books').on('click', getMyBooks);

async function getAllBooks(e){
    if (e){
        e.preventDefault(); 
    }
    $('#books').html('')

    res = await axios.get('/api/books');
    list = res.data.books;
    
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
            }
        }else{
            bookCard(book)
        }
    }
}

function bookCard(book){
    $('#books').append(`
    <div class="col-auto">
    <div class="card m-1" style="width: 18rem;">
        <img class="card-img-top" src="${book.cover}" alt="Card image cap">
        <div class="card-body">
          <h5 class="card-title">${book.title}</h5>
          <p class="card-text">${book.description}</p>
          <a href="#" class="btn btn-primary">Go To Book</a>
        </div>
      </div>
    </div>
    `)
}


getAllBooks()