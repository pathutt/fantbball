// Hides all the rows that are showing to prepare the table for new set of rows
function hideRows(){
    $('table tbody tr').each(function () {
        $(this).hide();
    })
}

// Shows all the rows on the specified table
function showAllRows(){
    $('table tbody tr').each(function () {
        $(this).show();
    })
}

// Filters rows out of the table based on position text
function showRows(target){
    $('table tbody tr').each(function () {
        if($(this).find('td').eq(4).text().indexOf(target) >= 0){
            $(this).show();
        }
    });
}

// Shows the hitter table if pitcher table is currently showing. Scrolls to the top of the table if available.
function showHitters(){
    $("#pitcher_table").hide();
    $("#hitter_table").show();
    $('.scrollTable').scrollTop(0);
}

// Shows the pitcher table if a hitter table is currently showing. Scrolls to the top of the table if available.
function showPitchers(){
    $("#hitter_table").hide();
    $("#pitcher_table").show();
    $('.scrollTable').scrollTop(0);
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

    // Loads the crossOutPNG on click and crosses or uncrosses out a row
    $('tbody tr').click(function (){
        $(this).toggleClass("crossedOut");
    });

    // Checks checkboxes based on the header columns. Header columns are generated from checked checkboxes on submit
    $('thead tr th').each(function(){
        let checkedId = $(this).text();
        if($('#' + checkedId).length >= 1 ) {
            $('#' + checkedId).prop('checked', true);
        };
    });

});