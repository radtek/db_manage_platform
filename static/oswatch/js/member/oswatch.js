;
var member_oswatch_ops = {
    init: function () {
       common_ops.changeMenu();
        this.eventBind();
    },
    eventBind: function () {
        $("#btn1").click(function () {
            $("#btn_name").val("btn_name_1");
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理！！请不要重复点击~~");
                return;
            }
            btn_target.addClass("disabled");
            $.ajax({
                url: common_ops.buildUrl("/oswatch/"),
                type: "POST",
                data: $('#form1').serialize(),
                dataType: "json",
                success: function (res) {
                    btn_target.removeClass("disabled");
                    common_ops.alert(res.msg);
                }
            });
        });
        $("#btn8").click(function () {
            $("#btn_name").val("btn_name_8");
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理！！请不要重复点击~~");
                return;
            }
            btn_target.addClass("disabled");
            $.ajax({
                url: common_ops.buildUrl("/oswatch/"),
                type: "POST",
                data: $('#form1').serialize(),
                dataType: "json",
                success: function (res) {
                    var callback = null;
                    if (res.code == 200) {
                        btn_target.removeClass("disabled");
                        callback = function () {
                            function addElement(mod,arr){
                                var osw_sec = document.getElementById('osw_sec');
                                var osw_result = document.getElementById('osw_result');
                                var new_osw_result = document.createElement('div');
                                if(osw_result == null){
                                    new_osw_result.id = 'osw_result';
                                    osw_sec.appendChild(new_osw_result);
                                }else{
                                     osw_result.remove();
                                     new_osw_result.id = 'osw_result';
                                     osw_sec.appendChild(new_osw_result);
                                }
                                for(var i = 0;i < arr.length;i++){
                                    var ele = document.createElement(mod);
                                    ele.setAttribute('src',arr[i]);
                                    new_osw_result.appendChild(ele);
                                }
                            }
                            var cpu_pic_path = '/static/osw/cpu_' + res.data.split('.')[3] + '.jpg' + '?tmp=' + Math.random();
                            var mem_pic_path = '/static/osw/mem_' + res.data.split('.')[3] + '.jpg' + '?tmp=' + Math.random();
                            var io_pic_path = '/static/osw/io_' + res.data.split('.')[3] + '.jpg' + '?tmp=' + Math.random();
                            var net_pic_path = '/static/osw/net_' + res.data.split('.')[3] + '.jpg' + '?tmp=' + Math.random();
                            arr = [cpu_pic_path,mem_pic_path,io_pic_path,net_pic_path];
                            addElement('img',arr);
                        };
                    }
                    common_ops.alert(res.msg, callback);
                }
            });
        });
    }
};

$(document).ready(function () {
    member_oswatch_ops.init();
});
