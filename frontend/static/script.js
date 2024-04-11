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
            $("#textArea1").val(data.message);
        });
    });
});