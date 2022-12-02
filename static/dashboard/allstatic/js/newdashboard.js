//daterange picker 1
$(function() {
  $('input[name="daterange1"]').daterangepicker({
      autoUpdateInput: false,
      locale: {
          cancelLabel: 'Clear'
      },
      autoApply: true
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
      },
      autoApply: true
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


// function showfilters() {
// var x = document.getElementById("hiddenfilters");
// if (x.style.display === "none") {
//   x.style.display = "block";
//   sessionStorage.setItem('clicked', true);
// }
//    else {
//   x.style.display = "none";
//   sessionStorage.setItem('clicked', false);
// }
// }


// window.onload = function () {
  
//   var data = sessionStorage.getItem('clicked');
//   if (data == 'true') {
//     x.style.display = "block";
//   }
// };
function showfilters() {
  document.getElementById('hiddenfilters').style.display = "block";
  let searchParams = new URLSearchParams(window.location.search);     
  localStorage.setItem('clicked', true);      
}

function closeFilters(){
  document.getElementById('hiddenfilters').style.display = "none";
  localStorage.removeItem('clicked');
}

// window.onload = function() {
//   var show = localStorage.getItem('clicked');
//   console.log(show)
//   if(clicked === true){
//        document.getElementById('hiddenfilters').style.display = "block";
//   }
// }

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
function graphDateRange(id){
  var x = document.getElementById(id);
      let searchParams = new URLSearchParams(window.location.search);
         if (searchParams.has("date_range") === true){
              searchParams.delete("date_range");
              
         }
         searchParams.append("date_range", x.getAttribute('data-value'));
       
     
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
function closeGraph(){
  let searchParams = new URLSearchParams(window.location.search);
         if (searchParams.has("key") === true){
          searchParams.delete("key");
          if(searchParams.has("id") === true){
            searchParams.delete("id");
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
              location.href = url;
            }
        }
}
function getOption() {
  selectElement = document.querySelector('#time-range');
  output = selectElement.options[selectElement.selectedIndex].value;
  document.querySelector('.output').textContent = output;
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
  let value = searchParams.get("category1");
  value = value.split(',');
  let index = value.indexOf(y.value); 
  if(index != -1){
    value.splice(index,1);
  }
  value = value.join(',');
  searchParams.set('category1', value);
}
else{
if(searchParams.has("category1")){
  let value = searchParams.get("category1");
  searchParams.set('category1', `${value},${y.value}`)
} else{
  searchParams.append('category1', `${y.value}`)
}
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
// keeps the checkbox checked 
var i = new URLSearchParams(window.location.search);
var types = i.get('category1');
if(types){
  types = types.split(",");
  
  document.querySelectorAll(".category1").forEach((elem)=>{
    if(types.includes(elem.value)){
        elem.setAttribute("checked", true)
    }
  })
}


var categorytwoValue = i.get('category2');
if(categorytwoValue){
  categorytwoValue = categorytwoValue.split(",");
  
  document.querySelectorAll(".category2").forEach((elem)=>{
    if(categorytwoValue.includes(elem.value)){
        elem.setAttribute("checked", true)
    }
  })
}

var competitorValue = i.get('competitor');
if(competitorValue){
  competitorValue = competitorValue.split(",");
  
  document.querySelectorAll(".competitor").forEach((elem)=>{
    if(competitorValue.includes(elem.value)){
        elem.setAttribute("checked", true)
    }
  })
}

var tagsValue = i.get('tags');
if(tagsValue){
  document.querySelector('#pt_filter_tags').value = tagsValue;
}
var trackingUrlValue = i.get('tracking_url');
if(trackingUrlValue){
  document.querySelector('#pt_filter_trackingUrl').value = trackingUrlValue;
}

var svLowValue = i.get('low');
if(svLowValue){
  document.querySelector('#pt_filter_svlow').value = svLowValue;
}
var svHighValue = i.get('high');
if(svHighValue){
  document.querySelector('#pt_filter_svhigh').value = svHighValue;
}
var DateRangeTwoValue = i.get('daterange2');
if(DateRangeTwoValue){
  document.querySelector('#pt_filter_daterange2').value = DateRangeTwoValue;
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
// if (searchParams.has("category2") === true){
//   searchParams.delete("category2");
// }
if(x == false){
  let value = searchParams.get("category2");
  value = value.split(',');
  let index = value.indexOf(y.value); 
  if(index != -1){
    value.splice(index,1);
  }
  value = value.join(',');
  searchParams.set('category2', value);
}
else{
// searchParams.append("category1", y.value);
if(searchParams.has("category2")){
  let value = searchParams.get("category2");
  searchParams.set('category2', `${value},${y.value}`)
} else{
  searchParams.append('category2', `${y.value}`)
}
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
// if (searchParams.has("competitor") === true){
//   searchParams.delete("competitor");
// }
if(x == false){
  let value = searchParams.get("competitor");
  value = value.split(',');
  let index = value.indexOf(y.value); 
  if(index != -1){
    value.splice(index,1);
  }
  value = value.join(',');
  searchParams.set('competitor', value);
}
else{
// searchParams.append("category1", y.value);
if(searchParams.has("competitor")){
  let value = searchParams.get("competitor");
  searchParams.set('competitor', `${value},${y.value}`)
} else{
  searchParams.append('competitor', `${y.value}`)
}
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
function clearCategory() {
   let searchParams = new URLSearchParams(window.location.search);
  
          searchParams.delete("category1");

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
function cleardateRangeOne() {
   let searchParams = new URLSearchParams(window.location.search);
  
          searchParams.delete("daterange1");

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
// // check if filter applied

  
  $(document).ready(function(){
    if ($("#appliedFilters").html().length > 0) {
      $('#appliedFilterscontainer').show();
    }       
    else{
      $('#appliedFilterscontainer').hide();
    }     

    if ($("#kpt-tags").html().length > 0) {
      $('#kpt-appliedFiltersTags').show();
    }       
    else{
      $('#kpt-appliedFiltersTags').hide();
    }     

    if ($("#kpt-url").html().length > 0) {
      $('#kpt-appliedFiltersUrl').show();
    }       
    else{
      $('#kpt-appliedFiltersUrl').hide();
    }     

    if ($("#kpt-sv").html().length > 0) {
      $('#kpt-appliedFiltersSv').show();
    }       
    else{
      $('#kpt-appliedFiltersSv').hide();
    }     

    if ($("#kpt-categoreis").html().length > 0) {
      $('#kpt-appliedFiltersCategories').show();
    }       
    else{
      $('#kpt-appliedFiltersCategories').hide();
    }     

    if ($("#kpt-competitor").html().length > 0) {
      $('#kpt-appliedFiltersComp').show();
    }       
    else{
      $('#kpt-appliedFiltersComp').hide();
    }     

    if ($("#kpt-daterange").html().length > 0) {
      $('#kpt-appliedFiltersDate').show();
    }       
    else{
      $('#kpt-appliedFiltersDate').hide();
    }       

    // document.querySelectorAll(".kpt-appliedFilters").forEach((elem)=>{
    //   if (elem.innerHTML.length > 0){
    //     $('.kpt-filter').show();
    //   }
    //   else{
    //     $('.kpt-filter').hide();
    //   }
    // })
  });
    // $("#wrapper").children().each(function(){
    //     if($(this).css('display') !== 'none')
    //     {
    //         $('#kpt-filterhead').show();
    //     }
    //     else{
    //         $('#kpt-filterhead').hide();
    //     }
    // });


// show applied filters

const queryString = window.location.search;
const urlParams = new URLSearchParams(queryString);
const timeRange = urlParams.get('time-range')
const timeRangeTwo = urlParams.get('time-range2')
const dateRangeOne = urlParams.get('daterange1')
const dateRangeTwo = urlParams.get('daterange2')
const category1 = urlParams.getAll('category1')
const category2 = urlParams.getAll('category2')
const tags = urlParams.getAll('tags')
const trackingUrl = urlParams.getAll('tracking_url')
const searchVolumeLow = urlParams.get('low')
const searchVolumeHigh = urlParams.get('high')
const competitor = urlParams.getAll('competitor')
const brand = urlParams.get('brand')

if(timeRange){
  document.getElementById("showfrequency").innerHTML = timeRange
}
if(timeRangeTwo){
  document.getElementById("showfrequency2").innerHTML = timeRangeTwo
}
if(dateRangeOne){
  document.getElementById("daterange1").value = dateRangeOne
}
if(dateRangeTwo){
  document.getElementById("kpt-daterange").innerHTML = dateRangeTwo
}
if(category1){
  document.getElementById("appliedFilters").innerHTML = category1
}
if(category2){
  document.getElementById("kpt-categoreis").innerHTML = category2
}
if(tags){
  document.getElementById("kpt-tags").innerHTML = tags
}
if(trackingUrl){
  document.getElementById("kpt-url").innerHTML = trackingUrl
}
if(searchVolumeLow || searchVolumeHigh){
  document.getElementById("kpt-sv").innerHTML = "Min : " + searchVolumeLow + " - " + "Max : " + searchVolumeHigh
} 
if(competitor){
  document.getElementById("kpt-competitor").innerHTML = competitor
}

if(brand){
  document.getElementById("show-brand").innerHTML = brand
}

function selectBrands(){
  var x = document.getElementById("selectBrand");
  
  let searchParams = new URLSearchParams(window.location.search);
  if (searchParams.has("brand") === true){
      searchParams.delete("brand");
  }
  searchParams.append("brand", x.value);
  
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