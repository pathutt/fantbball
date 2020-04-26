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

$(document).ready(function() {
    // Change active table
    $(".nav-link").click(function () {
        $(".nav-link").removeClass("active");
        $(this).addClass("active");
    });

    $("#hitters").click(function () {
        showAllRows();
    });

    $("#catcher").click(function () {
        hideRows();
        $('table tbody tr').each(function () {
            if($(this).find('td').eq(4).text() == "C"){
                $(this).show();
            }
        });
    });

    $("#1b").click(function () {
        hideRows();
        showRows("1B");
    });

    $("#2b").click(function () {
        hideRows();
        showRows("2B");
    });

    $("#3b").click(function () {
        hideRows();
        showRows("3B");
    });

    $("#ss").click(function () {
        hideRows();
        showRows("SS");
    });

    $("#of").click(function () {
        hideRows();
        showRows("LF");
        showRows("CF");
        showRows("RF");
    });

    $("#dh").click(function (){
        hideRows();
        showRows("DH");
    });

    $("#mi").click(function () {
        hideRows();
        showRows("2B");
        showRows("SS");
    });

    $("#ci").click(function () {
        hideRows();
        showRows("1B");
        showRows("3B");
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