;
var member_dataparse_ops = {
    init: function () {
       common_ops.changeMenu();
        this.eventBind();
    },
    eventBind: function () {
        $("#btn6").click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理！！请不要重复点击~~");
                return;
            }
            btn_target.addClass("disabled");
            $.ajax({
                url: common_ops.buildUrl("/oswatch/mon_pic"),
                type: "POST",
                data: $('#form3').serialize(),
                dataType: "json",
                success: function (res) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            var home = document.getElementById('home')
                            var pic_result = document.getElementById('pic_result');
                            if(pic_result == null){
                                var new_pic_result = document.createElement('div');
                                new_pic_result.setAttribute('id','pic_result');
                                home.appendChild(new_pic_result);
                            }else{
                                pic_result.remove();
                                var new_pic_result = document.createElement('div');
                                new_pic_result.setAttribute('id','pic_result');
                                home.appendChild(new_pic_result);
                            }
                            var mon_pic = document.createElement('img');
                            mon_pic.setAttribute('id','mon_pic');
                            var pic_path = '/static/pic/common.jpg' + '?tmp=' + Math.random();
                            mon_pic.setAttribute('src',pic_path);
                            new_pic_result.appendChild(mon_pic);
                        };
                    }
                    common_ops.alert(res.msg, callback);
                }
            });
        });
        $("#btn7").click(function () {
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理！！请不要重复点击~~");
                return;
            }
            btn_target.addClass("disabled");
            $.ajax({
                url: common_ops.buildUrl("/oswatch/mon_pic"),
                type: "POST",
                data: $('#form4').serialize(),
                dataType: "json",
                cache:false,
                success: function (res) {
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            var ios = document.getElementById('ios')
                            var pic_result = document.getElementById('pic_result');
                            if(pic_result == null){
                                var new_pic_result = document.createElement('div');
                                new_pic_result.setAttribute('id','pic_result');
                                ios.appendChild(new_pic_result);
                            }else{
                                pic_result.remove();
                                var new_pic_result = document.createElement('div');
                                new_pic_result.setAttribute('id','pic_result');
                                ios.appendChild(new_pic_result);
                            }
                            var mon_pic = document.createElement('img');
                            mon_pic.setAttribute('id','mon_pic');
                            var pic_path = '/static/pic/common.jpg' + '?tmp=' + Math.random();
                            mon_pic.setAttribute('src',pic_path);
                            new_pic_result.appendChild(mon_pic);
                        };
                    }
                    common_ops.alert(res.msg, callback);
                }
            });
        });
    }
};

$(document).ready(function () {
    member_dataparse_ops.init();
});