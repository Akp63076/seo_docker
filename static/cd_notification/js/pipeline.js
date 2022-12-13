var socket = io.connect('https://cdboards.in',{path:'/socket.io'}, {secure: true})
var switchh = document.getElementsByClassName('btn btn-secondary toggle')
for (i=0; i<switchh.length; i++){
    switchh[i].addEventListener('click', function(){
        if (this.parentElement.parentElement.classList.contains('done')){
            this.parentElement.parentElement.classList.remove('done')
            console.log(this.parentElement.parentElement.getElementsByTagName('p')[1].innerHTML)
            socket.emit(
                'undone', {
                    id: this.parentElement.parentElement.getElementsByTagName('p')[1].innerHTML,
                }   
            )
        }
        else {
            this.parentElement.parentElement.classList.add('done')
            this.parentElement.parentElement.getElementsByTagName('p')[1].innerHTML
            socket.emit(
                'done', {
                    id: this.parentElement.parentElement.getElementsByTagName('p')[1].innerHTML,
                }   
            )
        }      
    })
}

var layout = document.getElementById('myonoffswitch');
var tableDisplay = document.getElementById('table-content');
var gridDisplay = document.getElementById('grid-content');
function switchLayout(){
    console.log('It')
    if (layout.checked == false) {
	tableDisplay.style.display = "block"
        gridDisplay.style.display = "none"   
    }
    else {
	tableDisplay.style.display = "none"
        gridDisplay.style.display = "block"
    }
}


