window.onload = function(){
    // common_ops.changeMenu();
    function dbinstall(){
        // common_ops.changeMenu();
        var btn_target = $(this);
        if(btn_target.hasClass('disabled')){
            common_ops.alert('正在处理，请不要重复点击！');
            return;
        }
        btn_target.addClass('disabled');
        $.ajax({
           url:common_ops.buildUrl("/dbinstall/"),
           type:"POST",
           dataType:"json",
           data:{
               tag:'dbinstall'
           },
           success:function (res){
               btn_target.removeClass('disabled');
               var callback = null;
               if(res.code == 200){
                   callback = function (){

                   };
               }
               // common_ops.alert(res.msg,callback);
               }
        });
    }
    function dbcheck(){
        // common_ops.changeMenu();
        var btn_target = $(this);
        if(btn_target.hasClass('disabled')){
            common_ops.alert('正在处理，请不要重复点击！');
            return;
        }
        btn_target.addClass('disabled');
        $.ajax({
           url:common_ops.buildUrl("/dbinstall/"),
           type:"POST",
           dataType:"json",
           data:{
               tag:'dbcheck'
           },
           success:function (res){
               btn_target.removeClass('disabled');
               var callback = null;
               if(res.code == 200){
                   callback = function (){

                   };
               }
               // common_ops.alert(res.msg,callback);
               }
        });
    }
    function daily(){
        // common_ops.changeMenu();
        var btn_target = $(this);
        if(btn_target.hasClass('disabled')){
            common_ops.alert('正在处理，请不要重复点击！');
            return;
        }
        btn_target.addClass('disabled');
        $.ajax({
           url:common_ops.buildUrl("/dbinstall/"),
           type:"POST",
           dataType:"json",
           data:{
               tag:'daily'
           },
           success:function (res){
               btn_target.removeClass('disabled');
                var callback = null;
               if(res.code == 200){
                   callback = function (){

                   };
               }
               common_ops.alert(res.msg,callback);
               }
        });
    }
    // var btn = document.getElementById('new_dbinstall');
    // var btn_1 = document.getElementById('dbcheck');
    // var btn_2 = document.getElementById('daily');
    // btn.addEventListener('click',dbinstall,false);
    // btn_1.addEventListener('click',dbcheck,false);
    // btn_2.addEventListener('click',daily,false);
};