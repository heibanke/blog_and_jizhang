
    
    function gameLoop() {
        window.setTimeout(gameLoop, 20000);
        if(drawuser!=loginuser){
            getDraw(room_id);
        }
        getComment(room_id);
        getMember(room_id);
    } 
    
    //绘画函数
    function drowPad(e)
    {
       //aa=drawcolor.color();
       ctx.strokeStyle=drawcolor.color();
       ctx.save();
       ctx.beginPath();
       ctx.moveTo(x,y);
       ctx.lineTo(e.clientX-maginx,e.clientY-maginy); //cilentX获得的坐标是相对文档的坐标，我设置了mycanvas的边框为2像素，所以要减去2
       ctx.stroke();
       x = e.clientX-maginx;
       y = e.clientY-maginy;
       ctx.restore();
       xy.push({"x":x,"y":y});//把坐标添加到数组
       //tts.innerHTML = x+","+y;
    }

    //开始绘制的入口
    function startmove(e)
    {
        x = e.clientX-maginx; //获得鼠标按下的第一点的坐标
        y = e.clientY-maginy;
        xy.push({"x":x,"y":y});//添加到数组
        mycanvas.onmousemove = drowPad;//监听mycanvas的鼠标移动事件
        
    }

    //鼠标按键被放开时执行
    function stopmove(e)
    {
        mycanvas.onmousemove = null; //取消mycanvas鼠标移动监听事件
        //xy.push([0.1,0]);//把特定的值增加到数组，用于标记此次绘画结束，恢复绘画时用到
      
        postDraw(room_id);
    }       
    
    
    //根据数组记录的鼠标轨迹重新恢复画出的图形
    function drowDTX(json)
    {
        ctx.clearRect(0,0,mycanvas.width,mycanvas.height); //先清空mycanvas，避免累计绘制产生重叠
        ctx.save();
        
        //绘图
        if (json && json.length > 0) {
            for (var j = 0; j < json.length; j++){
                if (json[j].data != "None") {
                    draw = JSON.parse(json[j].data)
                    if(draw && draw.length>0){
                        ctx.strokeStyle = json[j].color
                        ctx.beginPath();
                        ctx.moveTo(draw[0].x,draw[0].y);
                        for (var i = 1; i < draw.length; i++){                            
                            ctx.lineTo(draw[i].x,draw[i].y);
                        }
                        ctx.stroke();    
                        ctx.closePath();
                    }
                }
            }
        }
        ctx.restore();
        
    }

    function clear_canvas(){
        xy = new Array();   
        drowDTX(xy);
    }


    function clearDraw(id) {
        var csrf=$("input[name='csrfmiddlewaretoken']").val();
        $.ajax({
            type: "POST",
            url: "/classroom/room/" + id + "/clear_draws/",
            dataType: "json",
            data: { csrfmiddlewaretoken:csrf },
            success: function(json) {
                if (json.success=='1'){
                    clear_canvas();
                }else{
                    $("#comment_div").append(json.message);
                }
            },
            error: function(res, textStatus, errorThrown) {
                $("#comment_div").append(res.responseText);
            }            
        });
    };   

    
    function postDraw(id) {
        var csrf=$("input[name='csrfmiddlewaretoken']").val();
        $.ajax({
            type: "POST",
            url: "/classroom/room/" + id + "/draws/",
            dataType: "json",
            data: { draw: JSON.stringify(xy),
                    color: drawcolor.color(),
                    csrfmiddlewaretoken:csrf },
            success: function(json) {
                //alert(1);
                xy = new Array();
            },
            error: function(res, textStatus, errorThrown) {
                $("#comment_div").append(res.responseText);
            }            
        });
    };    
    
    function getDraw(id) {
        var csrf=$("input[name='csrfmiddlewaretoken']").val();
        $.ajax({
            type: "GET",
            url: "/classroom/room/" + id + "/draws/",
            dataType: "json",
            data: { csrfmiddlewaretoken:csrf },
            success: function(json) {
                drowDTX(json);
            },
            error: function(res, textStatus, errorThrown) {
                $("#comment_div").append(res.responseText);
            }            
        });
    };         

    function postComment(id) {
        var textarea = $("#comment_content");
        var csrf=$("input[name='csrfmiddlewaretoken']").val();
        $.ajax({
            type: "POST",
            url: "/classroom/room/" + id + "/comments/",
            dataType: "json",
            data: { comment: textarea.val(),
                    csrfmiddlewaretoken:csrf },
            success: function(json) {
                showComments(json);
                textarea.val("");
            },
            error: function(res, textStatus, errorThrown) {
                $("#comment_div").append(res.responseText);
            }            
        });
    };

    function getComment(id) {
        var textarea = $("#comment_content");
        var csrf=$("input[name='csrfmiddlewaretoken']").val();
        $.ajax({
            type: "GET",
            url: "/classroom/room/" + id + "/comments/",
            dataType: "json",
            data: {csrfmiddlewaretoken:csrf },
            success: function(json) {
                showComments(json);
            },
            error: function(res, textStatus, errorThrown) {
                $("#comment_div").append(res.responseText);
            }            
        });
    };    

    function getMember(id) {
        var csrf=$("input[name='csrfmiddlewaretoken']").val();
        $.ajax({
            type: "GET",
            url: "/classroom/room/" + id + "/members/",
            dataType: "json",
            data: { csrfmiddlewaretoken:csrf },
            success: function(json) {
                showMembers(json);
            },
            error: function(res, textStatus, errorThrown) {
                $("#comment_div").append(res.responseText);
            }            
        });
    }; 
    
    var showComments = function(json) {
        var jDiv = $("#comment_div");
        jDiv.empty();
        if (json && json.length > 0) {
            for (var i = 0; i < json.length; i++)
                renderComment(jDiv, json[i]);

            jDiv.children().show();
        }
    };
    
    var showMembers = function(json) {
        var jDiv = $("#member_div");
        jDiv.empty();
        if (json && json.length > 0) {
            for (var i = 0; i < json.length; i++)
                jDiv.append('<p>'+json[i].user_display_name+'</p>');

            jDiv.children().show();
        }
    };    
    
    var renderComment = function(jDiv, json) {
        var html = '<div>' + json.text;
        html += ' <span>(' + json.user_display_name + ')</span>';
        html += ' <br/>(' + json.add_date + ')';

        if (json.delete_url) {
            html += ' <p>(' + json.delete_url + ')</p>';
        }else{
            html += ' <p></p>';
        }

        html += '</div>';

        jDiv.append(html);
    };   