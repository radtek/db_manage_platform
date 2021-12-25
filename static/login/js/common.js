;
var common_ops = {
    /* 切换标签设置活动标签样式 */
    changeMenu() {
        /* 找出class属性是active的，将其active class属性删除，然后给当前活动元素加上active类 */
        // const oldActiveA = document.querySelector('.active');
        // oldActiveA.removeAttribute('class', 'li.active');
        // currentEle.setAttribute('class', 'active');
        /* 从浏览器session中获取存储的当前菜单的id */
        const currentMenuId = sessionStorage.getItem('currentMenuId');
        if (!currentMenuId) { return; }
        const currentMenuELe = document.querySelector('#' + currentMenuId);
        const oldActiveA = document.querySelector('.active');
        oldActiveA.removeAttribute('class', 'li.active');
        currentMenuELe.setAttribute('class', 'active');
    },
    /* 跳转页面 */
    goPage(menuName) {
        sessionStorage.setItem('currentMenuId', menuName);
        // window.location.href = common_ops.buildUrl(url);
    },
    buildUrl:function( path ,params ){
        //params = { "test":"abc","sort":"asc" };
        // ?test=abc&sort=asc
        var url = "" + path;
        var _param_url = "";
        if( params ) {
            _param_url = Object.keys(params).map(function (k) {
                return [ encodeURIComponent(k),encodeURIComponent( params[k] ) ].join("=")
            }).join("&");
            _param_url = "?" + _param_url;
        }

        return url + _param_url;
    },
    alert:function( msg ,cb){
        layer.alert( msg,{
            offset:'400px',
            btn:['确定','取消'],
            yes:function( index ){
                if( typeof cb == "function" ){
                    cb();
                }
                layer.close( index );
            },
            no:function(index){
                layer.close(index);
            }
        } );
    },
    prompt_1: function(text,cb){
           layer.prompt({
                formType: 2,
                title: text,
                offset: '400px',
                area: ['1000px', '2000px'],
                btnAlign: 'c',
                content: `
                     <div style="width: 400px; height: auto">
                        <div style="text-align: center;margin-bottom: 12px">
                            <label style="display: inline-block;min-width: 10%;width: 30%;">请输入系统用户名:</label>
                            <input style="width: 220px;height: 30px" name="user" id="user">
                        </div>
                        <div style="text-align: center;margin-bottom: 12px">
                            <label style="display: inline-block;min-width: 10%;width: 30%;">请输入密码:</label>
                            <input style="width: 220px;height: 30px" name="pwd" id="pwd">
                        </div>
                        <div style="text-align: center;margin-bottom: 12px">
                            <label style="display: inline-block;min-width: 10%;width: 30%;">请输入ip地址:</label>
                            <input style="width: 220px;height: 30px" name="ip" id="ip">
                        </div>
                    </div>`,
               yes:function (index) {
                var user = $('#user').val();
                var pwd = $('#pwd').val();
                var ip = $('#ip').val();
                if( typeof cb == "function" ){
                    cb(user,pwd,ip);
                }
                layer.close(index);
                },
               no:function(index){
                    layer.close(index);
               }
           });
},
    prompt_2: function(text,cb){
           layer.prompt({
                formType: 2,
                title: text,
                offset: '80px',
                // area: ['500px', '400px'],
                btnAlign: 'c',
                content: `
                    <div style="width: 600px; height: auto">
                        <div style="text-align: center; margin-bottom: 5px">
                            <label style="display: inline-block;min-width: 10%;width: 20%;">oracle安装目录:</label>
                            <input name="ora_ins_dir" id="ora_ins_dir" style="width:300px;height:30px;">
                        </div>
                         <div style="text-align: center;margin-bottom: 5px">
                            <label style="display: inline-block;min-width: 10%;width: 20%;">oracle工具目录:</label>
                            <input style="width: 300px;height: 30px" name="ora_tool_dir" id="ora_tool_dir">
                         </div style="text-align: center;margin-bottom: 12px">
                         <div style="text-align: center;margin-bottom: 5px">
                            <label style="display: inline-block;min-width: 10%;width: 20%;">oracle数据目录:</label>
                            <input style="width: 300px;height: 30px" name="ora_data_dir" id="ora_data_dir">
                         </div>
                         <div style="text-align: center;margin-bottom: 5px">
                            <label style="display: inline-block;min-width: 10%;width: 20%;">oracle归档目录:</label>
                            <input style="width: 300px;height: 30px" name="ora_arch_dir" id="ora_arch_dir">
                         </div>
                         <div style="text-align: center;margin-bottom: 5px">
                            <label style="display: inline-block;min-width: 10%;width: 20%;">oracle_base目录:</label>
                            <input style="width: 300px;height: 30px" name="oracle_base" id="oracle_base">
                         </div>
                         <div style="text-align: center;margin-bottom: 5px">
                            <label style="display: inline-block;min-width: 10%;width: 20%;">oracle_home目录:</label>
                            <input style="width: 300px;height: 30px" name="oracle_home" id="oracle_home">
                         </div>
                         <div style="text-align: center;margin-bottom: 5px">
                            <label style="display: inline-block;min-width: 10%;width: 20%;">oracle用户密码:</label>
                            <input style="width: 300px;height: 30px" name="ora_pwd" id="ora_pwd">
                         </div>
                         <div style="text-align: center;margin-bottom: 5px">
                            <label style="display: inline-block;min-width: 10%;width: 20%;">数据库sid:</label>
                            <input style="width: 300px;height: 30px" name="ora_sid" id="ora_sid">
                         </div>
                         <div style="text-align: center;margin-bottom: 5px">
                            <label style="display: inline-block;min-width: 10%;width: 20%;">客户端字符集:</label>
                            <input style="width: 300px;height: 30px" name="client_lang" id="client_lang">
                         </div>
                         <div style="text-align: center;margin-bottom: 5px">
                            <label style="display: inline-block;min-width: 10%;width: 20%;">SGA大小:</label>
                            <input style="width: 300px;height: 30px" name="sga_size" id="sga_size">
                         </div>
                         <div style="text-align: center;margin-bottom: 5px">
                            <label style="display: inline-block;min-width: 10%;width: 20%;">ip地址:</label>
                            <input style="width: 300px;height: 30px" name="ip" id="ip">
                         </div>
                         <div style="text-align: center;margin-bottom: 5px">
                            <label style="display: inline-block;min-width: 10%;width: 20%;">主机名:</label>
                            <input style="width: 300px;height: 30px" name="host" id="host">
                         </div>
                         <div style="text-align: center;margin-bottom: 5px">
                            <label style="display: inline-block;min-width: 10%;width: 20%;">安装软件目录:</label>
                            <input style="width: 300px;height: 30px" name="soft_dir" id="soft_dir">
                         </div>
                         <div style="text-align: center;margin-bottom: 5px">
                            <label style="display: inline-block;min-width: 10%;width: 20%;">root用户密码:</label>
                            <input style="width: 300px;height: 30px" name="root_pwd" id="root_pwd">
                         </div>
                         <div style="text-align: center;margin-bottom: 5px">
                            <label style="display: inline-block;min-width: 10%;width: 20%;">db安装软件:</label>
                            <input style="width: 300px;height: 30px" name="db_soft" id="db_soft">
                         </div>
                         <div style="text-align: center;margin-bottom: 5px">
                            <label style="display: inline-block;min-width: 10%;width: 20%;">sys用户密码:</label>
                            <input style="width: 300px;height: 30px" name="sys_pwd" id="sys_pwd">
                         </div>
                         <div style="text-align: center;margin-bottom: 5px">
                            <label style="display: inline-block;min-width: 10%;width: 20%;">system用户密码:</label>
                            <input style="width: 300px;height: 30px" name="system_pwd" id="system_pwd">
                         </div>
                         <div style="text-align: center;margin-bottom: 5px">
                            <label style="display: inline-block;min-width: 10%;width: 20%;">数据库总内存:</label>
                            <input style="width: 300px;height: 30px" name="db_mem" id="db_mem">
                         </div>
                         <div style="text-align: center;margin-bottom: 5px">
                            <label style="display: inline-block;min-width: 10%;width: 20%;">数据库字符集:</label>
                            <input style="width: 300px;height: 30px" name="db_lang" id="db_lang">
                         </div>
                         <div style="text-align: center;margin-bottom: 5px">
                            <label style="display: inline-block;min-width: 10%;width: 20%;">opatch文件:</label>
                            <input style="width: 300px;height: 30px" name="opatch_file" id="opatch_file">
                         </div>
                         <div style="text-align: center;margin-bottom: 5px">
                            <label style="display: inline-block;min-width: 10%;width: 20%;">补丁文件:</label>
                            <input style="width: 300px;height: 30px" name="opatch" id="opatch">
                        </div>
                    </div>`,
                yes:function (index) {
                var ora_ins_dir = $('#ora_ins_dir').val();
                var ora_tool_dir = $('#ora_tool_dir').val();
                var ora_data_dir = $('#ora_data_dir').val();
                var ora_arch_dir = $('#ora_arch_dir').val();
                var oracle_base = $('#oracle_base').val();
                var oracle_home = $('#oracle_home').val();
                var ora_pwd = $('#ora_pwd').val();
                var ora_sid = $('#ora_sid').val();
                var client_lang = $('#client_lang').val();
                var sga_size = $('#sga_size').val();
                var ip = $('#ip').val();
                var host = $('#host').val();
                var soft_dir = $('#soft_dir').val();
                var root_pwd = $('#root_pwd').val();
                var db_soft = $('#db_soft').val();
                var sys_pwd = $('#sys_pwd').val();
                var system_pwd = $('#system_pwd').val();
                var db_mem = $('#db_mem').val();
                var db_lang = $('#db_lang').val();
                var opatch_file = $('#opatch_file').val();
                var opatch = $('#opatch').val();
                var db_install_info = [ora_ins_dir,ora_tool_dir,ora_data_dir,ora_arch_dir,oracle_base,oracle_home,ora_pwd,ora_sid,client_lang,sga_size,ip,host,soft_dir,root_pwd,db_soft,sys_pwd,system_pwd,db_mem,db_lang,opatch_file,opatch];
                if( typeof cb == "function" ){
                    cb(db_install_info);
                }
                layer.close(index);
                },
               no:function(index){
                    layer.close(index);
               }
           });
},
    pop_tab:function(text,data) {
        layer.prompt({
            formType: 2,
            title: text,
            offset: '400px',
            area: ['1000px', '2000px'],
            btnAlign: 'c',
            content: `
                     <div id="tb_result">
                        是否查看结果？
                     </div>
                     `,
            yes: function (index) {
                console.log(typeof data);
                if (text == '实例启动时间') {
                    var table = document.createElement('table');
                    table.setAttribute('id', 'tb')
                    table.setAttribute('border', '5px')
                    var tr = document.createElement('tr');
                    var th_0 = document.createElement('th');
                    var th_1 = document.createElement('th');
                    var th_2 = document.createElement('th');
                    var th_3 = document.createElement('th');
                    th_0.innerHTML = 'ip地址';
                    th_1.innerHTML = '实例名';
                    th_2.innerHTML = '开始时间';
                    th_3.innerHTML = '结束时间';
                    var tb_result = document.getElementById('tb_result');
                    tb_result.innerHTML = null;
                    tb_result.appendChild(table);
                    table.appendChild(tr);
                    tr.appendChild(th_0);
                    tr.appendChild(th_1);
                    tr.appendChild(th_2);
                    tr.appendChild(th_3);
                    var tb = document.getElementById('tb');
                    for (var i = 0; i < data.length; i++) {
                        console.log(data[i]);
                        var row = document.createElement('tr');
                        var idCell_0 = document.createElement('td');
                        idCell_0.innerHTML = data[i][0];
                        var idCell_1 = document.createElement('td');
                        idCell_1.innerHTML = data[i][1];
                        var idCell_2 = document.createElement('td');
                        idCell_2.innerHTML = data[i][2];
                        var idCell_3 = document.createElement('td');
                        idCell_3.innerHTML = data[i][3];
                        tb.appendChild(row);
                        row.appendChild(idCell_0);
                        row.appendChild(idCell_1);
                        row.appendChild(idCell_2);
                        row.appendChild(idCell_3);
                    }
                }
                if (text == '表空间检查') {
                    var table = document.createElement('table');
                    table.setAttribute('id', 'tb')
                    table.setAttribute('border', '1px')
                    var tr = document.createElement('tr');
                    var th_0 = document.createElement('th');
                    var th_1 = document.createElement('th');
                    var th_2 = document.createElement('th');
                    var th_3 = document.createElement('th');
                    var th_4 = document.createElement('th');
                    var th_5 = document.createElement('th');
                    var th_6 = document.createElement('th');
                    var th_7 = document.createElement('th');
                    th_0.innerHTML = 'IP';
                    th_1.innerHTML = 'TABLESPACE_NAME';
                    th_2.innerHTML = 'TOTAL_MB';
                    th_3.innerHTML = 'FREE_MB';
                    th_4.innerHTML = 'USED_MB';
                    th_5.innerHTML = 'FREE_RATIO';
                    th_6.innerHTML = 'USED_RATIO';
                    th_7.innerHTML = 'GETTIME';
                    var tb_result = document.getElementById('tb_result');
                    tb_result.innerHTML = null;
                    tb_result.appendChild(table);
                    table.appendChild(tr);
                    tr.appendChild(th_0);
                    tr.appendChild(th_1);
                    tr.appendChild(th_2);
                    tr.appendChild(th_3);
                    tr.appendChild(th_4);
                    tr.appendChild(th_5);
                    tr.appendChild(th_6);
                    tr.appendChild(th_7);
                    var tb = document.getElementById('tb');
                    for (var i = 0; i < data.length; i++) {
                        console.log(data[i]);
                        var row = document.createElement('tr');
                        var idCell_0 = document.createElement('td');
                        idCell_0.innerHTML = data[i][0];
                        var idCell_1 = document.createElement('td');
                        idCell_1.innerHTML = data[i][1];
                        var idCell_2 = document.createElement('td');
                        idCell_2.innerHTML = data[i][2];
                        var idCell_3 = document.createElement('td');
                        idCell_3.innerHTML = data[i][3];
                        var idCell_4 = document.createElement('td');
                        idCell_4.innerHTML = data[i][3];
                        var idCell_5 = document.createElement('td');
                        idCell_5.innerHTML = data[i][3];
                        var idCell_6 = document.createElement('td');
                        idCell_6.innerHTML = data[i][3];
                        var idCell_7 = document.createElement('td');
                        idCell_7.innerHTML = data[i][3];
                        tb.appendChild(row);
                        row.appendChild(idCell_0);
                        row.appendChild(idCell_1);
                        row.appendChild(idCell_2);
                        row.appendChild(idCell_3);
                        row.appendChild(idCell_4);
                        row.appendChild(idCell_5);
                        row.appendChild(idCell_6);
                        row.appendChild(idCell_7);
                    }
                }
                if (text == '更新对象检查') {
                    var table = document.createElement('table');
                    table.setAttribute('id', 'tb')
                    table.setAttribute('border', '1px')
                    var tr = document.createElement('tr');
                    var th_0 = document.createElement('th');
                    var th_1 = document.createElement('th');
                    var th_2 = document.createElement('th');
                    th_0.innerHTML = 'IP';
                    th_1.innerHTML = '更新对象个数';
                    th_2.innerHTML = '获取时间';
                    var tb_result = document.getElementById('tb_result');
                    tb_result.innerHTML = null;
                    tb_result.appendChild(table);
                    table.appendChild(tr);
                    tr.appendChild(th_0);
                    tr.appendChild(th_1);
                    tr.appendChild(th_2);
                    var tb = document.getElementById('tb');
                    for (var i = 0; i < data.length; i++) {
                        console.log(data[i]);
                        var row = document.createElement('tr');
                        var idCell_0 = document.createElement('td');
                        idCell_0.innerHTML = data[i][0];
                        var idCell_1 = document.createElement('td');
                        idCell_1.innerHTML = data[i][1];
                        var idCell_2 = document.createElement('td');
                        idCell_2.innerHTML = data[i][2];
                        tb.appendChild(row);
                        row.appendChild(idCell_0);
                        row.appendChild(idCell_1);
                        row.appendChild(idCell_2);
                    }
                }
                if (text == '作业调度检查') {
                    var table = document.createElement('table');
                    table.setAttribute('id', 'tb')
                    table.setAttribute('border', '1px')
                    var tr = document.createElement('tr');
                    var th_0 = document.createElement('th');
                    var th_1 = document.createElement('th');
                    var th_2 = document.createElement('th');
                    var th_3 = document.createElement('th');
                    var th_4 = document.createElement('th');
                    var th_5 = document.createElement('th');
                    var th_6 = document.createElement('th');
                    var th_7 = document.createElement('th');
                    var th_8 = document.createElement('th');
                    var th_9 = document.createElement('th');
                    th_0.innerHTML = 'IP';
                    th_1.innerHTML = 'LOG_DATE';
                    th_2.innerHTML = 'OWNER';
                    th_3.innerHTML = 'JOB_NAME';
                    th_4.innerHTML = 'STATUS';
                    th_5.innerHTML = 'ERROR#';
                    th_6.innerHTML = 'RUN_DURATION';
                    th_7.innerHTML = 'CPU_USED';
                    th_8.innerHTML = 'ADDITIONAL_INFO';
                    th_9.innerHTML = 'GETTIME';
                    var tb_result = document.getElementById('tb_result');
                    tb_result.innerHTML = null;
                    tb_result.appendChild(table);
                    table.appendChild(tr);
                    tr.appendChild(th_0);
                    tr.appendChild(th_1);
                    tr.appendChild(th_2);
                    tr.appendChild(th_3);
                    tr.appendChild(th_4);
                    tr.appendChild(th_5);
                    tr.appendChild(th_6);
                    tr.appendChild(th_7);
                    tr.appendChild(th_8);
                    tr.appendChild(th_9);
                    var tb = document.getElementById('tb');
                    for (var i = 0; i < data.length; i++) {
                        console.log(data[i]);
                        var row = document.createElement('tr');
                        var idCell_0 = document.createElement('td');
                        idCell_0.innerHTML = data[i][0];
                        var idCell_1 = document.createElement('td');
                        idCell_1.innerHTML = data[i][1];
                        var idCell_2 = document.createElement('td');
                        idCell_2.innerHTML = data[i][2];
                        var idCell_3 = document.createElement('td');
                        idCell_3.innerHTML = data[i][3];
                        var idCell_4 = document.createElement('td');
                        idCell_4.innerHTML = data[i][4];
                        var idCell_5 = document.createElement('td');
                        idCell_5.innerHTML = data[i][5];
                        var idCell_6 = document.createElement('td');
                        idCell_6.innerHTML = data[i][6];
                        var idCell_7 = document.createElement('td');
                        idCell_7.innerHTML = data[i][7];
                        var idCell_8 = document.createElement('td');
                        idCell_8.innerHTML = data[i][8];
                        var idCell_9 = document.createElement('td');
                        idCell_9.innerHTML = data[i][9];
                        tb.appendChild(row);
                        row.appendChild(idCell_0);
                        row.appendChild(idCell_1);
                        row.appendChild(idCell_2);
                        row.appendChild(idCell_3);
                        row.appendChild(idCell_4);
                        row.appendChild(idCell_5);
                        row.appendChild(idCell_6);
                        row.appendChild(idCell_7);
                        row.appendChild(idCell_8);
                        row.appendChild(idCell_9);
                    }
                }
                if(text == '备份检查'){
                    var table = document.createElement('table');
                    table.setAttribute('id', 'tb')
                    table.setAttribute('border', '1px')
                    var tr = document.createElement('tr');
                    var th_0 = document.createElement('th');
                    var th_1 = document.createElement('th');
                    var th_2 = document.createElement('th');
                    var th_3 = document.createElement('th');
                    th_0.innerHTML = 'IP';
                    th_1.innerHTML = 'START_TIME';
                    th_2.innerHTML = 'END_TIME';
                    th_3.innerHTML = 'STATUS';
                    var tb_result = document.getElementById('tb_result');
                    tb_result.innerHTML = null;
                    tb_result.appendChild(table);
                    table.appendChild(tr);
                    tr.appendChild(th_0);
                    tr.appendChild(th_1);
                    tr.appendChild(th_2);
                    tr.appendChild(th_3);
                    var tb = document.getElementById('tb');
                    for (var i = 0; i < data.length; i++) {
                        console.log(data[i]);
                        var row = document.createElement('tr');
                        var idCell_0 = document.createElement('td');
                        idCell_0.innerHTML = data[i][0];
                        var idCell_1 = document.createElement('td');
                        idCell_1.innerHTML = data[i][1];
                        var idCell_2 = document.createElement('td');
                        idCell_2.innerHTML = data[i][2];
                        var idCell_3 = document.createElement('td');
                        idCell_3.innerHTML = data[i][3];
                        tb.appendChild(row);
                        row.appendChild(idCell_0);
                        row.appendChild(idCell_1);
                        row.appendChild(idCell_2);
                        row.appendChild(idCell_3);
                    }
                }
                if(text == '归档检查'){
                    var table = document.createElement('table');
                    table.setAttribute('id', 'tb')
                    table.setAttribute('border', '1px')
                    var tr = document.createElement('tr');
                    var th_0 = document.createElement('th');
                    var th_1 = document.createElement('th');
                    var th_2 = document.createElement('th');
                    th_0.innerHTML = 'IP';
                    th_1.innerHTML = 'A';
                    th_2.innerHTML = 'GETTIME';
                    var tb_result = document.getElementById('tb_result');
                    tb_result.innerHTML = null;
                    tb_result.appendChild(table);
                    table.appendChild(tr);
                    tr.appendChild(th_0);
                    tr.appendChild(th_1);
                    tr.appendChild(th_2);
                    var tb = document.getElementById('tb');
                    for (var i = 0; i < data.length; i++) {
                        console.log(data[i]);
                        var row = document.createElement('tr');
                        var idCell_0 = document.createElement('td');
                        idCell_0.innerHTML = data[i][0];
                        var idCell_1 = document.createElement('td');
                        idCell_1.innerHTML = data[i][1];
                        var idCell_2 = document.createElement('td');
                        idCell_2.innerHTML = data[i][2];
                        tb.appendChild(row);
                        row.appendChild(idCell_0);
                        row.appendChild(idCell_1);
                        row.appendChild(idCell_2);
                    }
                }
                if(text == '性能检查'){
                    var table = document.createElement('table');
                    table.setAttribute('id', 'tb')
                    table.setAttribute('border', '1px')
                    var tr = document.createElement('tr');
                    var th_0 = document.createElement('th');
                    var th_1 = document.createElement('th');
                    var th_2 = document.createElement('th');
                    th_0.innerHTML = 'IP';
                    th_1.innerHTML = 'HIT';
                    th_2.innerHTML = 'GETTIME';
                    var tb_result = document.getElementById('tb_result');
                    tb_result.innerHTML = null;
                    tb_result.appendChild(table);
                    table.appendChild(tr);
                    tr.appendChild(th_0);
                    tr.appendChild(th_1);
                    tr.appendChild(th_2);
                    var tb = document.getElementById('tb');
                    for (var i = 0; i < data.length; i++) {
                        console.log(data[i]);
                        var row = document.createElement('tr');
                        var idCell_0 = document.createElement('td');
                        idCell_0.innerHTML = data[i][0];
                        var idCell_1 = document.createElement('td');
                        idCell_1.innerHTML = data[i][1];
                        var idCell_2 = document.createElement('td');
                        idCell_2.innerHTML = data[i][2];
                        tb.appendChild(row);
                        row.appendChild(idCell_0);
                        row.appendChild(idCell_1);
                        row.appendChild(idCell_2);
                    }
                }
                if(text == '表空间报表' || text == 'aas报表'){
                    var img = document.createElement('img');
                    img.setAttribute('src','/static/pic/common.jpg' + '?tmp=' + Math.random());
                    var tb_result = document.getElementById('tb_result');
                    tb_result.innerHTML = null;
                    tb_result.appendChild(img);
                }
                if(text == 'sqlserver巡检'){
                    var img = document.createElement('img');
                    img.setAttribute('src','/static/sqlserver/sqlserver.jpg' + '?tmp=' + Math.random());
                    var tb_result = document.getElementById('tb_result');
                    tb_result.innerHTML = null;
                    tb_result.appendChild(img);
                }
                // layer.close(index);
                },
               no:function(index){
                    layer.close(index);
               }
           });
    },
    prompt_k: function(text,cb){
           layer.prompt({
                formType: 2,
                title: text,
                offset: '400px',
                area: ['1000px', '2000px'],
                btnAlign: 'c',
                content: `
                     <div style="width: 400px; height: auto">
                        <div style="text-align: center;margin-bottom: 12px">
                            <label style="display: inline-block;min-width: 10%;width: 30%;">请输入IP地址:</label>
                            <input style="width: 220px;height: 30px" name="ip" id="ip">
                        </div>
                        <div style="text-align: center;margin-bottom: 12px">
                            <label style="display: inline-block;min-width: 10%;width: 30%;">请输入时间:</label>
                            <input style="width: 220px;height: 30px" name="tm" id="tm">
                        </div>
                    </div>`,
               yes:function (index) {
                var ip = $('#ip').val();
                var tm = $('#tm').val();
                if( typeof cb == "function" ){
                    cb(ip,tm);
                }
                layer.close(index);
                },
               no:function(index){
                    layer.close(index);
               }
           });
},
    prompt_abs: function(text,cb){
           layer.prompt({
                formType: 2,
                title: text,
                offset: '400px',
                area: ['1000px', '2000px'],
                btnAlign: 'c',
                content: `
                     <div style="width: 400px; height: auto">
                        <div style="text-align: center;margin-bottom: 12px">
                            <label style="display: inline-block;min-width: 10%;width: 30%;">请输入IP地址:</label>
                            <input style="width: 220px;height: 30px" name="ip" id="ip">
                        </div>
                        <div style="text-align: center;margin-bottom: 12px">
                            <label style="display: inline-block;min-width: 10%;width: 30%;">请输入表空间名称:</label>
                            <input style="width: 220px;height: 30px" name="tbs" id="tbs">
                        </div>
                        <div style="text-align: center;margin-bottom: 12px">
                            <label style="display: inline-block;min-width: 10%;width: 30%;">请输入时间:</label>
                            <input style="width: 220px;height: 30px" name="tm" id="tm">
                        </div>
                    </div>`,
               yes:function (index) {
                var ip = $('#ip').val();
                var tbs = $('#tbs').val();
                var tm = $('#tm').val();
                if( typeof cb == "function" ){
                    cb(ip,tbs,tm);
                }
                layer.close(index);
                },
               no:function(index){
                    layer.close(index);
               }
           });
    }
}
