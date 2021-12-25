window.onload = function(){
    common_ops.changeMenu();
    function sqlserver_oper(){
           var btn_target = $(this);
           if(btn_target.hasClass('disabled')){
               common_ops.alert('正在处理！请不要重复点击！');
               return ;
           }
           btn_target.addClass('disabled');
           $.ajax({
               url:common_ops.buildUrl("/dbcheck/sqlservercheck"),
               type:"POST",
               dataType:"json",
               data:{},
               success:function (res){
                   btn_target.removeClass('disabled');
                   var callback = null;
                   if(res.code == 200){
                       callback = function (){
                            var home = document.getElementById('home');
                            var sqlserver_div = document.getElementById('sqlserver_div');
                            var new_sqlserver_div = document.createElement('div');
                            if(sqlserver_div == null){
                                new_sqlserver_div.setAttribute('id','sqlserver_div');
                                home.appendChild(new_sqlserver_div);
                            }else{
                                sqlserver_div.remove();
                                new_sqlserver_div.setAttribute('id','sqlserver_div');
                                home.appendChild(new_sqlserver_div);
                            }
                            var img = document.createElement('img');
                            img.setAttribute('src','/static/sqlserver/sqlserver.jpg' + '?tmp=' + Math.random());
                            new_sqlserver_div.appendChild(img);
                       };
                   }
                   common_ops.alert(res.msg,callback);
               }
           });
    }
    var sqlserver_btn = document.getElementById('sqlserver_btn');
    sqlserver_btn.addEventListener('click',sqlserver_oper,false);
};