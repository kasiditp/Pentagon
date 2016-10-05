/**
 * Created by FTTX on 10/5/2016 AD.
 */

var already_filtered = {size:null,max_price:null,brand:null};

function filter() {
    var element = $(this);
    console.log(element);
    // if(event.split("_")[0] == "size")
    //     already_filtered.size = event.split("_")[1]
    // else if(event == "max")
    //     already_filtered.max_price = event
    //
    // $.ajax({
    //     url : '/filter/',
    //     type : 'GET',
    //     data : event
    // })
}

$('size_s').on('click',filter());