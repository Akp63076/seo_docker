//daterange picker 1
$(function() {
  $('input[name="daterange1"]').daterangepicker({
      autoUpdateInput: false,
      locale: {
          cancelLabel: 'Clear'
      }
  }); 
  $('input[name="daterange1"]').on('apply.daterangepicker', function(ev, picker) {
      $(this).val(picker.startDate.format('DD/MM/YYYY') + ' - ' + picker.endDate.format('DD/MM/YYYY'));
  });
  $('input[name="daterange1"]').on('cancel.daterangepicker', function(ev, picker) {
      $(this).val('');
  });
});

//daterange picker 2
$(function() {
  $('input[name="daterange2"]').daterangepicker({
      autoUpdateInput: false,
      locale: {
          cancelLabel: 'Clear'
      }
  });
  $('input[name="daterange2"]').on('apply.daterangepicker', function(ev, picker) {
      $(this).val(picker.startDate.format('DD/MM/YYYY') + ' - ' + picker.endDate.format('DD/MM/YYYY'));
  });
  $('input[name="daterange2"]').on('cancel.daterangepicker', function(ev, picker) {
      $(this).val('');
  });
});

//daterange end 
$(document).ready(function () {
  $("#test").CreateMultiCheckBox({ width: '230px', defaultText : 'Select Below', height:'250px' });
});
    //checkbox drop down
    $(".checkbox-dropdown").click(function () {
      $(this).toggleClass("is-active");
    });
    $(".checkbox-dropdown ul").click(function (e) {
      e.stopPropagation();
    });
    $(document).ready(function () {
      $(document).on("click", ".MultiCheckBox", function () {
          var detail = $(this).next();
          detail.show();   
      });
      $(document).on("click", ".MultiCheckBoxDetailHeader input", function (e) {
          e.stopPropagation();
          var hc = $(this).prop("checked");
          $(this).closest(".MultiCheckBoxDetail").find(".MultiCheckBoxDetailBody input").prop("checked", hc);
          $(this).closest(".MultiCheckBoxDetail").next().UpdateSelect();
      });
      $(document).on("click", ".MultiCheckBoxDetailHeader", function (e) {
          var inp = $(this).find("input");
          var chk = inp.prop("checked");
          inp.prop("checked", !chk);
          $(this).closest(".MultiCheckBoxDetail").find(".MultiCheckBoxDetailBody input").prop("checked", !chk);
          $(this).closest(".MultiCheckBoxDetail").next().UpdateSelect();
      });
      $(document).on("click", ".MultiCheckBoxDetail .cont input", function (e) {
          e.stopPropagation();
          $(this).closest(".MultiCheckBoxDetail").next().UpdateSelect();
          var val = ($(".MultiCheckBoxDetailBody input:checked").length == $(".MultiCheckBoxDetailBody input").length)
          $(".MultiCheckBoxDetailHeader input").prop("checked", val);
      });
      $(document).on("click", ".MultiCheckBoxDetail .cont", function (e) {
          var inp = $(this).find("input");
          var chk = inp.prop("checked");
          inp.prop("checked", !chk);
          var multiCheckBoxDetail = $(this).closest(".MultiCheckBoxDetail");
          var multiCheckBoxDetailBody = $(this).closest(".MultiCheckBoxDetailBody");
          multiCheckBoxDetail.next().UpdateSelect();
          var val = ($(".MultiCheckBoxDetailBody input:checked").length == $(".MultiCheckBoxDetailBody input").length)
          $(".MultiCheckBoxDetailHeader input").prop("checked", val);
      });
      $(document).mouseup(function (e) {
          var container = $(".MultiCheckBoxDetail");
          if (!container.is(e.target) && container.has(e.target).length === 0) {
              container.hide();
          }
      });
  });
  var defaultMultiCheckBoxOption = { width: '220px', defaultText: 'Select Below', height: '200px' };
  jQuery.fn.extend({
      CreateMultiCheckBox: function (options) {
          var localOption = {};
          localOption.width = (options != null && options.width != null && options.width != undefined) ? options.width : defaultMultiCheckBoxOption.width;
          localOption.defaultText = (options != null && options.defaultText != null && options.defaultText != undefined) ? options.defaultText : defaultMultiCheckBoxOption.defaultText;
          localOption.height = (options != null && options.height != null && options.height != undefined) ? options.height : defaultMultiCheckBoxOption.height;
          this.hide();
          this.attr("multiple", "multiple");
          var divSel = $("<div class='MultiCheckBox'>" + localOption.defaultText + "<span class='k-icon k-i-arrow-60-down'><svg aria-hidden='true' focusable='false' data-prefix='fas' data-icon='sort-down' role='img' xmlns='http://www.w3.org/2000/svg' viewBox='0 0 320 512' class='svg-inline--fa fa-sort-down fa-w-10 fa-2x'><path fill='currentColor' d='M41 288h238c21.4 0 32.1 25.9 17 41L177 448c-9.4 9.4-24.6 9.4-33.9 0L24 329c-15.1-15.1-4.4-41 17-41z' class=''></path></svg></span></div>").insertBefore(this);
          divSel.css({ "width": localOption.width });

          var detail = $("<div class='MultiCheckBoxDetail'><div class='MultiCheckBoxDetailHeader'><input type='checkbox' class='mulinput' value='-1982' /><div>Select All</div></div><div class='MultiCheckBoxDetailBody'></div></div>").insertAfter(divSel);
          detail.css({ "width": parseInt(options.width) + 10, "max-height": localOption.height });
          var multiCheckBoxDetailBody = detail.find(".MultiCheckBoxDetailBody");

          this.find("option").each(function () {
              var val = $(this).attr("value");

              if (val == undefined)
                  val = '';

              multiCheckBoxDetailBody.append("<div class='cont'><div><input type='checkbox' class='mulinput' value='" + val + "' /></div><div>" + $(this).text() + "</div></div>");
          });

          multiCheckBoxDetailBody.css("max-height", (parseInt($(".MultiCheckBoxDetail").css("max-height")) - 28) + "px");
      },
      UpdateSelect: function () {
          var arr = [];
          this.prev().find(".mulinput:checked").each(function () {
              arr.push($(this).val());
          });
          this.val(arr);
      },
  });

  // filters
  function showfilters() {
var x = document.getElementById("hiddenfilters");
if (x.style.display === "none") {
  x.style.display = "block";
} else {
  x.style.display = "none";
}
}

//search filter  
function keywordSearch() {
var input, filter, table, tr, td, i, txtValue;
input = document.getElementById("keyword-search");
filter = input.value.toUpperCase();
table = document.getElementById("positiontable");
tr = table.getElementsByClassName("datarow");
for (i = 0; i < tr.length; i++) {
  td = tr[i].getElementsByTagName("td")[0];
  if (td) {
    txtValue = td.textContent || td.innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      tr[i].style.display = "";
    } else {
      tr[i].style.display = "none";
    }
  }       
}
}


// trend graph
window.onload = function(){
let searchParams = new URLSearchParams(window.location.search);
         if (searchParams.has("key") === true){
          const Params = new Proxy(new URLSearchParams(window.location.search), {
            get: (searchParams, prop) => searchParams.get(prop),
          });           
          let id = Params.id;
          var x = document.getElementById("graphrow"+ id);
           x.style.display = "grid";
         }
         
}


function trendgraph(id) {  
     var x = document.getElementById("key"+ id);
      let searchParams = new URLSearchParams(window.location.search);
         if (searchParams.has("key") === true){
             searchParams.delete("key");
             searchParams.delete("id");  
         }
         searchParams.append("key", x.value);
         searchParams.append("id", id);
     
         if (window.history.replaceState) {
             const url = window.location.protocol 
                         + "//" + window.location.host 
                         + window.location.pathname 
                         + "?" 
                         + searchParams.toString();
     
             window.history.replaceState({
                 path: url
             }, "", url)
             location.href = url;
            }   
     }
// upper tabl frequency
function frequency() {
var x = document.getElementById("time-range");

let searchParams = new URLSearchParams(window.location.search);
if (searchParams.has("time-range") === true){
    searchParams.delete("time-range");
}
searchParams.append("time-range", x.value);

if (window.history.replaceState) {
    const url = window.location.protocol 
                + "//" + window.location.host 
                + window.location.pathname 
                + "?" 
                + searchParams.toString();

    window.history.replaceState({
        path: url
    }, "", url)
    location.href = url;
}
}
function frequencyTwo() {
var x = document.getElementById("timerange2");

let searchParams = new URLSearchParams(window.location.search);
if (searchParams.has("time-range2") === true){
    searchParams.delete("time-range2");
}
searchParams.append("time-range2", x.value);

if (window.history.replaceState) {
    const url = window.location.protocol 
                + "//" + window.location.host 
                + window.location.pathname 
                + "?" 
                + searchParams.toString();

    window.history.replaceState({
        path: url
    }, "", url)
    location.href = url;
}
}

// upper table daterange

function dateRange() {
var x = document.getElementById("daterange1");

let searchParams = new URLSearchParams(window.location.search);
if (searchParams.has("daterange1") === true){
    searchParams.delete("daterange1");
}
searchParams.append("daterange1", x.value);

if (window.history.replaceState) {
    const url = window.location.protocol 
                + "//" + window.location.host 
                + window.location.pathname 
                + "?" 
                + searchParams.toString();

    window.history.replaceState({
        path: url
    }, "", url)
    location.href = url;
}

}
function formappend(id){

var y = document.getElementById(id);
var x = document.getElementById(id).checked;

let searchParams = new URLSearchParams(window.location.search);
if(x == false){
searchParams.delete("category1");

}
else{
searchParams.append("category1", y.value);
}
if (window.history.replaceState) {
   const url = window.location.protocol 
               + "//" + window.location.host 
               + window.location.pathname 
               + "?" 
               + searchParams.toString();

   window.history.replaceState({
       path: url
   }, "", url)

}
}
//upper table  apply button for checkbox filter
function applyfilters(){
var url = window.location.href
location.href = url;
}
// position table append 
function ptCheckboxAppendOne(id){
var y = document.getElementById(id);
var x = document.getElementById(id).checked; 

let searchParams = new URLSearchParams(window.location.search);
if (searchParams.has("category2") === true){
  searchParams.delete("category2");
}
if(x == false){
searchParams.delete("category2");
}
else{
  searchParams.append("category2", y.value);
}
 if (window.history.replaceState) {
     const url = window.location.protocol 
                 + "//" + window.location.host 
                 + window.location.pathname 
                 + "?" 
                 + searchParams.toString();

     window.history.replaceState({
         path: url
     }, "", url)
}
}
function ptCheckboxAppendTwo(id){
var y = document.getElementById(id);
var x = document.getElementById(id).checked; 

let searchParams = new URLSearchParams(window.location.search);
if (searchParams.has("competitor") === true){
  searchParams.delete("competitor");
}
if(x == false){
searchParams.delete("competitor");
}
else{
  searchParams.append("competitor", y.value);
}
 if (window.history.replaceState) {
     const url = window.location.protocol 
                 + "//" + window.location.host 
                 + window.location.pathname 
                 + "?" 
                 + searchParams.toString();

     window.history.replaceState({
         path: url
     }, "", url)
}
}

function positionTableFilter(){
var a = document.getElementById("pt_filter_tags");
var b = document.getElementById("pt_filter_trackingUrl");
var c = document.getElementById("pt_filter_svlow");
var d = document.getElementById("pt_filter_svhigh");
var e = document.getElementById("pt_filter_daterange2");
let searchParams = new URLSearchParams(window.location.search);

if (searchParams.has("tags") === true){
  searchParams.delete("tags");
}
searchParams.append("tags", a.value);

if (searchParams.has("tracking_url") === true){
  searchParams.delete("tracking_url");
}
searchParams.append("tracking_url", b.value);

if (searchParams.has("low") === true){
  searchParams.delete("low");
}
searchParams.append("low", c.value);

if (searchParams.has("high") === true){
  searchParams.delete("high");
}
searchParams.append("high", d.value);

if (searchParams.has("daterange2") === true){
  searchParams.delete("daterange2");
}
searchParams.append("daterange2", e.value);

if (window.history.replaceState) {
  const url = window.location.protocol 
              + "//" + window.location.host 
              + window.location.pathname 
              + "?" 
              + searchParams.toString();

  window.history.replaceState({
      path: url
  }, "", url)
  location.href = url;
}
}
function rowCounter(id){
var x = document.getElementById("row-counter");

let searchParams = new URLSearchParams(window.location.search);
if (searchParams.has("row-counter") === true){
    searchParams.delete("row-counter");
}
searchParams.append("row-counter", x.value);

if (window.history.replaceState) {
    const url = window.location.protocol 
                + "//" + window.location.host 
                + window.location.pathname 
                + "?" 
                + searchParams.toString();

    window.history.replaceState({
        path: url
    }, "", url)
    location.href = url;
}
}

function pagination(id){
var x = document.getElementById( id);
      let searchParams = new URLSearchParams(window.location.search);
         if (searchParams.has("page") === true){
              searchParams.delete("page");
              
         }
         searchParams.append("page", x.getAttribute('data-value'));
       
     
         if (window.history.replaceState) {
             const url = window.location.protocol 
                         + "//" + window.location.host 
                         + window.location.pathname 
                         + "?" 
                         + searchParams.toString();
     
             window.history.replaceState({
                 path: url
             }, "", url)
             location.href = url;
            }   
     }
     function removePage(){
      let searchParams = new URLSearchParams(window.location.search);
      if (searchParams.has("page") === true){
           searchParams.delete("page");
      } 
      }
// clear filters

function clearFilters() {
   let searchParams = new URLSearchParams(window.location.search);
  
          searchParams.delete("tags");
          searchParams.delete("tracking_url");
          searchParams.delete("low");
          searchParams.delete("high");
          searchParams.delete("daterange2");
          searchParams.delete("competitor");
          searchParams.delete("category2");
           

      if (window.history.replaceState) {
          const url = window.location.protocol 
                      + "//" + window.location.host 
                      + window.location.pathname 
                      + "?" 
                      + searchParams.toString();
  
          window.history.replaceState({
              path: url
          }, "", url)
          location.href = url;
         }   
  }
