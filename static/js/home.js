function hideRows(){
    $('table tbody tr').each(function () {
        $(this).hide();
    })
}

function showAllRows(){
    $('table tbody tr').each(function () {
        $(this).show();
    })
}

function showRows(target){
    $('table tbody tr').each(function () {
        if($(this).find('td').eq(4).text().indexOf(target) >= 0){
            $(this).show();
        }
    });
}

function showHitters(){
    $("#pitcher_table").hide();
    $("#hitter_table").show();
}

function showPitchers(){
    $("#hitter_table").hide();
    $("#pitcher_table").show();
}

$(document).ready(function() {
    // Change active table
    $(".nav-link").click(function () {
        $(".nav-link").removeClass("active");
        $(this).addClass("active");
    });

    $("#hitters").click(function () {
        showAllRows();
        showHitters();
    });

    $("#pitchers").click(function () {
        showAllRows();
        showPitchers();
    });

    $("#catcher").click(function () {
        showHitters();
        hideRows();
        $('table tbody tr').each(function () {
            if($(this).find('td').eq(4).text() == "C"){
                $(this).show();
            }
        });
    });

    $("#1b").click(function () {
        showHitters();
        hideRows();
        showRows("1B");
    });

    $("#2b").click(function () {
        showHitters();
        hideRows();
        showRows("2B");
    });

    $("#3b").click(function () {
        showHitters();
        hideRows();
        showRows("3B");
    });

    $("#ss").click(function () {
        showHitters();
        hideRows();
        showRows("SS");
    });

    $("#of").click(function () {
        showHitters();
        hideRows();
        showRows("LF");
        showRows("CF");
        showRows("RF");
    });

    $("#dh").click(function (){
        showHitters();
        hideRows();
        showRows("DH");
    });

    $("#mi").click(function () {
        showHitters();
        hideRows();
        showRows("2B");
        showRows("SS");
    });

    $("#ci").click(function () {
        showHitters();
        hideRows();
        showRows("1B");
        showRows("3B");
    });

    $("#sp").click(function () {
        showPitchers();
        hideRows();
        showRows("SP");
    });

    $("#rp").click(function () {
        showPitchers();
        hideRows();
        showRows("RP");
    });

    $('tbody tr').click(function (){
        $(this).toggleClass("crossedOut");
    });

    $('thead tr th').each(function(){
        let checkedId = $(this).text();
        if($('#' + checkedId).length >= 1 ) {
            $('#' + checkedId).prop('checked', true);
        };
    });

    // $('.form-check-input').each(function () {
    //         let status = localStorage.getItem(this.id) === "false" ? false : true;
    //         if(status){
    //             this.prop('checked');
    //         } else {
    //             this.removeAttr('checked');
    //         }
    // });
    //
    // $(".post-btn").click(function () {
    //     $('.form-check-input').each(function () {
    //         if($(this).is('checked')){
    //             localStorage.setItem(this.id, "true");
    //         } else {
    //             localStorage.setItem(this.id, "false");
    //         }
    //
    //     });
    // });

});

// $( window ).on( "load", function() {
//     $('thead tr th').each(function(){
//         let checkedId = $(this).text();
//         if($('#' + checkedId).length >= 1 ) {
//             $('#' + checkedId).prop('checked', true);
//         };
//     });
// });