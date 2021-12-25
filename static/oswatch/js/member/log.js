;
var member_log_ops = {
    init: function () {
       common_ops.changeMenu();
        this.eventBind();
    },
    eventBind: function () {
        $("#btn2").click(function () {
            $("#btn_name2").val("btn_name_2");
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理！！请不要重复点击~~");
                return;
            }
            btn_target.addClass("disabled");
            $.ajax({
                url: common_ops.buildUrl("/oswatch/log_oper"),
                type: "POST",
                data: $('#form2').serialize(),
                dataType: "json",
                success: function (res) {
                    btn_target.removeClass("disabled");
                    common_ops.alert(res.msg);
                }
            });
        });
        $("#btn3").click(function () {
            $("#btn_name2").val("btn_name_3");
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理！！请不要重复点击~~");
                return;
            }
            btn_target.addClass("disabled");
            $.ajax({
                url: common_ops.buildUrl("/oswatch/log_oper"),
                type: "POST",
                data: $('#form2').serialize(),
                dataType: "json",
                success: function (res) {
                   var callback = null;
                    if (res.code == 200) {
                        btn_target.removeClass("disabled");
                        callback = function () {
                            var ele = document.getElementById("text")
                            ele.value = res.data
                        };
                    }
                    common_ops.alert(res.msg, callback);
                }
            });
        });
        $("#btn4").click(function () {
            $("#btn_name2").val("btn_name_4");
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理！！请不要重复点击~~");
                return;
            }
            btn_target.addClass("disabled");
            $.ajax({
                url: common_ops.buildUrl("/oswatch/log_oper"),
                type: "POST",
                data: $('#form2').serialize(),
                dataType: "json",
                success: function (res) {
                    btn_target.removeClass("disabled");
                    common_ops.alert(res.msg);
                }
            });
        });
        $("#btn5").click(function () {
            $("#btn_name2").val("btn_name_5");
            var btn_target = $(this);
            if (btn_target.hasClass("disabled")) {
                common_ops.alert("正在处理！！请不要重复点击~~");
                return;
            }
            btn_target.addClass("disabled");
            $.ajax({
                url: common_ops.buildUrl("/oswatch/log_oper"),
                type: "POST",
                data: $('#form2').serialize(),
                dataType: "json",
                success: function (res) {
                    var callback = null;
                    if (res.code == 200) {
                        btn_target.removeClass("disabled");
                        callback = function () {
                            var ele = document.getElementById("text")
                            ele.value = res.data
                        };
                    }
                    common_ops.alert(res.msg, callback);
                }
            });
        });
    }
};

$(document).ready(function () {
    member_log_ops.init();
});