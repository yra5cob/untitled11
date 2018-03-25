/**
 * Created by Yeswanth Kumar on 3/23/2018.
 */
var a
var audio
function btnClick(lnk, id, title) {
    //post("/index",{link:lnk});
    $.post("player",
        {
            link: lnk

        },
        function (data, status) {
            var url = data;
            var newdiv1 = $('<li><a href="#" data-title="' + title + '" data-src="' + url + '">' + title + '</a></li>');
            $("ol").append(newdiv1);
            $('ol li').click(function (e) {
                document.getElementById("titl").innerHTML = '<h1><em>' + $('a', this).attr('data-title') + '</em></h1>';
                e.preventDefault();
                $(this).addClass('playing').siblings().removeClass('playing');
                audio = a[0];
                audio.load($('a', this).attr('data-src'));
                audio.play();
            });
            newdiv1.click();
        });
}
function btnAdd(lnk, id, title) {
    //post("/index",{link:lnk});
    $.post("player",
        {
            link: lnk

        },
        function (data, status) {
            var url = data;
            var newdiv1 = $('<li><a href="#" data-title="' + title + '" data-src="' + url + '">' + title + '</a></li>');
            $("ol").append(newdiv1);
            $('ol li').click(function (e) {
                document.getElementById("titl").innerHTML = '<h1><em>' + $('a', this).attr('data-title') + '</em></h1>';
                e.preventDefault();
                $(this).addClass('playing').siblings().removeClass('playing');
                audio = a[0];
                audio.load($('a', this).attr('data-src'));
                audio.play();
            });
        });

}
$(function () {
    // Setup the player to autoplay the next track
    a = audiojs.createAll({
        trackEnded: function () {
            var next = $('ol li.playing').next();
            if (!next.length) next = $('ol li').first();
            next.addClass('playing').siblings().removeClass('playing');
            audio.load($('a', next).attr('data-src'));
            document.getElementById("titl").innerHTML = '<h1><em>' + $('a', next).attr('data-title') + '</em></h1>';
            audio.play();
        }
    });

    // Load in the first track


    // Load in a track on click
    $('ol li').click(function (e) {
        document.getElementById("titl").innerHTML = '<h1><em>' + $('a', this).attr('data-title') + '</em></h1>';
        e.preventDefault();
        $(this).addClass('playing').siblings().removeClass('playing');
        audio.load($('a', this).attr('data-src'));
        audio.play();
    });
    // Keyboard shortcuts
    $(document).keydown(function (e) {
        var unicode = e.charCode ? e.charCode : e.keyCode;
        // right arrow
        if (unicode == 39) {
            var next = $('li.playing').next();
            if (!next.length) next = $('ol li').first();
            next.click();
            // back arrow
        } else if (unicode == 37) {
            var prev = $('li.playing').prev();
            if (!prev.length) prev = $('ol li').last();
            prev.click();
            // spacebar
        }
    })
});

//search ajax request
function search() {
    $('#holder').hide();
    $("#searchResult").html("<div id='holder'><img src='/static/loading-icon.gif'/></div>");
    var query = $('#search').val();
    $.post("search",
        {
            squery: query

        },
        function (data, status) {
            $("#searchResult").html(data);
        });

}

$(document).ready(function () {
    console.log("ready!");

    $('#search').keypress(function (e) {
        var key = e.which;
        if (key == 13)  // the enter key code
        {
            search();
            return false;
        }
    });
    $('#searchbtn').click(function () {
        console.log("here");
        search();
    });
});