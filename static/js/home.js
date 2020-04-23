$(document).ready(function() {
    // Change active table
    $(".nav-link").click(function() {
        $(".nav-link").removeClass("active");
        $(this).addClass("active");
    })

    $("#catcher").click(function() {
        $.ajax
        ({
            url: '/catcher',
            type: 'get'
        });
    })

    $(".post-btn").click(function() {
        $.ajax
        ({
            url: '/',
            type: 'post'
        });
    })
});