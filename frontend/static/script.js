type = null;
/* particlesJS.load(@dom-id, @path-json, @callback (optional)); */
particlesJS.load('particles-js', 'static/particlesjs-config.json', function() {
    console.log('callback - particles.js config loaded');
});

$(document).ready(function() {
    $(".navbar-toggler").click(function() {
        // 移除按钮的焦点
        $(this).blur();
    });
});

$(document).ready(function() {
    // 綁定按鈕點擊事件
    $("#mp3_btn").click(function() {
        // 獲取輸入框中的 URL
        var url = $("#url").val();

        // 使用 AJAX 發送 GET 請求
        $.ajax({
            url: "http://localhost:8000/",
            type: "GET",
            data: { 
                url: url,
                type: "mp3"
            }
        }).then(function(data) {
            $("#res_msg").val(data.message);
        });
    });
});

$(document).ready(function() {
    $(".button").click(function() {
        // 將所有按鈕恢復原始樣式
        $(".button").removeClass("active");
        
        type = $(this).text();

        // 將點擊的按鈕添加 active 類，改變其外觀
        $(this).addClass("active");
    });
});

$(document).ready(function() {
    $("#clr_btn").click(function() {
        $(".button").removeClass("active");
        type = null;
        $("#url").val("");
    });
});

$(document).ready(function() {
    $("#submit_btn").click(function() {
        // 獲取輸入框中的 URL
        var url = $("#url").val();

        // 使用 AJAX 發送 GET 請求
        $.ajax({
            url: "http://localhost:8000/",
            type: "GET",
            data: { 
                url: url,
                type: type
            }
        }).then(function(data) {
            $("#res_msg").val(data.message);
        });
    });
});
 