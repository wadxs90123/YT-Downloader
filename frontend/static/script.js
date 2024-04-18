api_server = "http://127.0.0.1:8000"
api2_server = "http://127.0.0.1:4000"
src_type = null; 
video_id = null;


function sleep (time) {
    return new Promise((resolve) => setTimeout(resolve, time));
}

particlesJS.load('particles-js', 'static/particlesjs-config.json', function() {
    console.log('callback - particles.js config loaded');
});

function downloadReset(){
    $("#download").prop("disabled", true);
    $("#res-msg").val(""); 
}

function changeStyle(clickedButton) {
    var buttons = document.querySelectorAll('.mybtn'); 
     
    buttons.forEach(function(button) {
        if (button === clickedButton) { 
            button.classList.add('mybtn-active');
            src_type = button.textContent.toLowerCase();
        } else { 
            button.classList.remove('mybtn-active');
        }
    });
}

$(document).ready(function() {    
    document.getElementById('download').addEventListener("change", function() {
        if (this.disabled) {
            this.style.cursor = "not-allowed";
        } else {
            this.style.cursor = "pointer";
        }
    });

    // 移除按鈕的焦點
    $(".navbar-toggler").click(function() {
        $(this).blur();
    });
    
    // 綁定清除按鈕點擊事件
    $("#btn_clear").click(function() {
        $(".mybtn").removeClass("mybtn-active");
        src_type = null; 
        video_id = null;
        $("#url").val("");
        downloadReset();
    });

    // 綁定按鈕點擊事件
    $("#btn_submit").click(function() {
        if(src_type == null){
            alert("Please select a type!");
            return;
        }
        // 獲取輸入框中的 URL
        var url = $("#url").val();

        // 如果 URL 為空，則提示用戶輸入 URL
        if(url == ""){
            alert("Please input a URL!");
            return;
        }

        // 禁止按鈕
        $("#btn_submit").prop("disabled", true);
        $("#btn_clear").prop("disabled", true);

        // 顯示處理中訊息
        var counter = 0;
        var processInterval = setInterval(function(){
            counter++;
            var dots = ".".repeat(counter % 3 + 1);
            $("#res-msg").val("Processing" + dots);
        }, 500);

        var progressInterval = setInterval(function(){
            // Create WebSocket connection
            var ws = new WebSocket('ws://localhost:8765') 
            // 在開啟連線時執行
            ws.onopen = () => {
                console.log('[open connection]')
                ws.send("hello server!!!")
                // Listen for messages from Server
                ws.onmessage = event => {
                    // $("#progress").val(event.data);
                    $("#progress-bar").val(parseInt(event.data));
                    if(src_type == "wmv" && event.data == 99) {
                        $("#res-msg").val("convert to wmv...");
                        clearInterval(processInterval);
                        clearInterval(progressInterval);
                    }
                    console.log(`[Message from server]:\n %c${event.data}` , 'color: blue')
                    ws.close() ;
                }
            }
        }, 500);

        $.ajax({ 
            url: `${api_server}/download?url=${encodeURIComponent(url)}&type=${src_type}`,
            type: "GET" 
        }).then(function(data) {
            $("#res-msg").val(data.message);
            video_id = data.name;
            $("#download").prop("disabled", false);
            $("#btn_submit").prop("disabled", false);
            $("#btn_clear").prop("disabled", false);
            clearInterval(processInterval);
            $("#progress-bar").val(100);
            clearInterval(progressInterval);
        }).catch(function(err) {
            $("#res-msg").val(err.responseJSON.message);
            $("#download").prop("disabled", true);
            $("#btn_submit").prop("disabled", false);
            $("#btn_clear").prop("disabled", false);
            clearInterval(processInterval);
            clearInterval(progressInterval);
        }) ;
    });

    // 下載按鈕點擊事件
    $("#download").click(function() {
        if ($(this).prop("disabled") || video_id == null) {
            return;
        }

        $.ajax({
            url: `${api_server}/video/${video_id}/name`,
            type: "GET",
        }).then(function(data) {
            if(data.message != "Success"){
                $("#res-msg").val(data.message);
                return;
            }
            var originalName = data.name;
            var originalName = originalName.replace(/ /g, "_");//把空格替換成底線
          
            $.ajax({
                url: `${api_server}/video/${video_id}`,
                type: "GET",
                xhrFields: {
                    responseType: 'blob'  
                }
            }).then(function(response, status, xhr) {
                var contentType = xhr.getResponseHeader('Content-Type');  
                var extension = contentType.split('/')[1];  
                if(extension == "mpeg"){
                    extension = "mp3";
                }else if(extension == "x-ms-wmv"){
                    extension = "wmv";
                }
                var fileName = `${originalName}.${extension}`;  
        
                var blob = new Blob([response], { type: contentType });
                var blobURL = window.URL.createObjectURL(blob);
        
                
                var a = document.createElement('a');
                a.href = blobURL;
                a.download = fileName; 
        
            
                a.click();
        
                window.URL.revokeObjectURL(blobURL);
            }).catch(function(err) {
                $("#res-msg").val(err.responseJSON.message);
                $("#download").prop("disabled", true);
            });
        }); 
    });    
});