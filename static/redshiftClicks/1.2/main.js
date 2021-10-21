
var myVar;
var counter = 0;

// https://blog.miguelgrinberg.com/post/using-celery-with-flask
// var nanobar = new Nanobar({
//     bg: '#44f',
//     target: document.getElementById("progress_bar")
// });



document.getElementById("start-bg-job").addEventListener("click", function (e) {
      $.ajax({
          type: "POST",
          url: "/redshiftClicks/start/",
          data: $("#searchForm").serialize(), // serializes the form's elements.
          success: function(data,status, request) {

            document.getElementById('start-bg-job').style.display='none';
            document.getElementById('successbtn').innerHTML='<button class="btn btn-success" id="ongoingjob"  disabled>Success!</button>';
            document.getElementById('includedContent').style.display='none';
              
              status_url = "/redshiftClicks/status/"+data.task_id+"/";
              console.log(data.task_id)
              console.log(document.location.href)
              console.log(status_url)
            //   
              update_progress_2(status_url);
              alert("Congratulations your query has been recieved");

            //   url_result = document.getElementById('url_result');
            //   var result_link = "https://sacp.cdboards.in/result/"+data;
              
            //   url_result.innerHTML = "<p>click on the below link, if <ul><li>You are going to close the tab</li></ul></p><a href="+result_link + " target='_blank' rel='noopener noreferrer'>Result page link</a>"
              console.log(status)
              document.getElementById('statuscontent').innerHTML="<p><b>NOTE: </b>Your query has been submitted successfully, This will take some time. </p><p>After the query completion </p><ul><li>The data will be displayed below, so don't close the current tab</li><li>You will also receive data on your mail (Make sure your mail id is current).</li></ul>"
          },
          error: function() {
                    alert('Unexpected error');}
      });
      e.preventDefault(); // avoid to execute the actual submit of the form.
  });

function update_progress_2(status_url) {
    $.ajax({
        type: "Get",
        url: status_url,
        dataType: "json",
        success: function(data) {
            // console.log(status_url);
            document.getElementById('includedContent').innerHTML = '<div class="inner-container"><div class="wrap"><div class="control-label col-sm-"><h4>Redshift-Data</h4></div><div id="here_table"></div> </div></div>';
            document.getElementById('progress-info').innerHTML = "<h5> STATUS OF TASK : "+data['state']+"</h5>"
            console.log(data['current']);
            // nanobar.go(counter);
            console.log(data);
            if (data['state'] != 'PENDING' && data['state'] != 'PROGRESS' && data['state'] !="ALMOST THERE") {

                if ('result' in data) {
                    // show result
                    myStopFunction();
                    console.log("built_table")
                    table_formation(data)
                    alert("Task is completed")
                  
                    }
                else {
                    // something unexpected happened
                    alert("Something went wrong");
                    
                }

            }
            
            else {
                // rerun in 2 seconds
                myVar = setTimeout(function() {
                    update_progress_2(status_url);
                    counter = counter+1;
                },2000);
            }



        },
        error: function(request, status, error){
            alert("Check your internet,Click Retry");
        }
    })
    
};


function myStopFunction() {
  clearTimeout(myVar);
}

function retry(){
    update_progress_2(status_url)
}



function table_formation(data){

    var doc = document;
    // display of data
    console.log(data) 
    
    
    //fetch user url and append to table-container
    var user_url_value = document.getElementById("form-linkID").value;
    var user_url = document.createElement('h4');
    user_url.innerHTML = "Query Link : "+user_url_value
    // fetch data lenth and show length of results appending to table-container
    var len_of_result = data['result'].length;
    var redshit_length = document.createElement('h5');
    redshit_length.innerHTML = "About "+ len_of_result +" results";
    
    // fetch results from data
    var array = data['result'];

    // table head
    var thead = document.createElement('thead')
    $(thead).addClass("thead-dark")
    var tr = document.createElement('tr');
    tr.innerHTML = "<th>Outgoing Link</th><th>Anchor Text</th><th>Click Count</th>"
    thead.appendChild(tr);  
    
    // table body
    var tbody = document.createElement('tbody'), tr, td;
    var x;
    for ( x in array){
        var array_elem = array[x];
        tr = document.createElement('tr');
        for ( inner_data in array_elem ){
            var value = array_elem[inner_data];
            td = document.createElement('td');
            tr.appendChild(td);
            td.innerHTML = value;       
    }
    tbody.appendChild(tr)
    }
    $(tbody).addClass("table-striped")

    // table class is created and thead and tbody append to this
    var table = doc.createElement("table");
    $(table).addClass("table table-bordered table-hover")
    table.append(thead)
    table.append(tbody)
    
    var table_container = doc.createElement("table-container");
    table_container.append(user_url)
    table_container.append(redshit_length)
    table_container.append(table)
    // table container contains table user url and length of data
    doc.getElementById("here_table").appendChild(table_container);
    document.getElementById('includedContent').style.display='block'
}

