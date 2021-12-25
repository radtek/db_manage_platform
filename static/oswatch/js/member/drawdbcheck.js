var canvas = document.getElementById("dbcheck_canvas");
var cxt = canvas.getContext('2d');
var canWidth = cxt.canvas.clientWidth;
var init = {top: 32, spaceH: 70};
var row2 = {
    data:[
        {
            type:'Step',
            text:'oracle巡检工具',
            name:'step_2_1',
            arrowArr:[
                    {
                        arrow:'drawBottomToTop',
                        to:'step_3_1'
                    },
                    {
                        arrow:'drawBottomToTop',
                        to:'step_3_2'
                    },
                {
                        arrow:'drawBottomToTop',
                        to:'step_3_3'
                    },
                {
                        arrow:'drawBottomToTop',
                        to:'step_3_4'
                    },
                {
                        arrow:'drawBottomToTop',
                        to:'step_3_5'
                    },
                {
                        arrow:'drawBottomToTop',
                        to:'step_3_6'
                    },
                {
                        arrow:'drawBottomToTop',
                        to:'step_3_7'
                    }
                ],
            x:'',
            y:'',
            requestData:{}
        }
    ]
};

var row3 = {
    data:[
        {
            type:'Step',
            text:'实例启动时间',
            name:'step_3_1',
            arrowArr:[
                    {
                        arrow:'drawBottomToTop',
                        to:'step_4_1'
                    }
                ],
            x:'',
            y:'',
            requestData:{}
        },
        {
            type:'Step',
            text:'表空间检查',
            name:'step_3_2',
            arrowArr:[
                    {
                        arrow:'drawBottomToTop',
                        to:'step_4_1'
                    }
                ],
        },
        {
            type:'Step',
            text:'更新对象检查',
            name:'step_3_3',
            arrowArr:[
                    {
                        arrow:'drawBottomToTop',
                        to:'step_4_1'
                    }
                ],
        },
        {
            type:'Step',
            text:'作业调度检查',
            name:'step_3_4',
            arrowArr:[
                    {
                        arrow:'drawBottomToTop',
                        to:'step_4_1'
                    }
                ],
        },
        {
            type:'Step',
            text:'备份检查',
            name:'step_3_5',
            arrowArr:[
                    {
                        arrow:'drawBottomToTop',
                        to:'step_4_1'
                    }
                ],
        },
        {
            type:'Step',
            text:'归档检查',
            name:'step_3_6',
            arrowArr:[
                    {
                        arrow:'drawBottomToTop',
                        to:'step_4_1'
                    }
                ],
        },
        {
            type:'Step',
            text:'性能检查',
            name:'step_3_7',
            arrowArr:[
                    {
                        arrow:'drawBottomToTop',
                        to:'step_4_1'
                    }
                ],
        }
    ]
};

var row5 = {
    data:[
        {
            type:'Step',
            text:'表空间报表',
            name:'step_5_1',
            arrowArr:[
                    {
                        arrow:'drawBottomToTop',
                        to:'step_6_1'
                    }
                ],
            x:'',
            y:'',
            requestData:{},
            method: {
            onmousemove: null,
            onmouseleave: null,
            onclick: db_abs
        }
        },
        {
            type:'Step',
            text:'aas报表',
            name:'step_5_2',
            arrowArr:[
                    {
                        arrow:'drawBottomToTop',
                        to:'step_6_1'
                    }
                ],
            method: {
            onmousemove: null,
            onmouseleave: null,
            onclick: tab_pop
        }
        },
    ]
};
row2.data = calChartX(canWidth,row2.data, row2.y);
row3.data = calChartX(canWidth,row3.data, row3.y);
row5.data = calChartX(canWidth,row5.data, row5.y);

var flowData = [
    {
        row:1,
        y:init.top,
        data:[
            {
                type:'Start',
                text:'巡检工具',
                name:'step_1_1',
                arrowArr:[
                    {
                        arrow:'drawBottomToTop',
                        to:'step_2_1'
                    }
                ],
                x:canWidth/2,
                y:''
            }
        ]
    },
    {
        row: 2,
        data: row2.data
    },
    {
        row: 3,
        data: row3.data,
        method: {
            onmousemove: null,
            onmouseleave: null,
            onclick: tab_pop
        }
    },
    {
        row:4,
        data:[
            {
                type:'Step',
                text:'oracle报表工具',
                name:'step_4_1',
                arrowArr:[
                    {
                        arrow:'drawBottomToTop',
                        to:'step_5_1'
                    },
                    {
                        arrow:'drawBottomToTop',
                        to:'step_5_2'
                    }
                ],
                x:canWidth/2,
                y:''
            }
        ]
    },
     {
        row: 5,
        data: row5.data
    },
    {
        row:6,
        data:[
            {
                type:'Step',
                text:'sqlserver巡检工具',
                name:'step_6_1',
                arrowArr:[
                    {
                        arrow:'drawBottomToTop',
                        to:'step_7_1'
                    }
                ],
                x:canWidth/2,
                y:''
            }
        ]
    },
    {
        row:7,
        data:[
            {
                type:'Step',
                text:'sqlserver巡检',
                name:'step_7_1',
                arrowArr:null,
                x:canWidth/2,
                y:''
            }
        ],
        method: {
            onmousemove: null,
            onmouseleave: null,
            onclick: sqlserver_check
        }
    }
];

drawFlowChart(cxt,canvas,flowData, init.top, init.spaceH);

function tab_pop(singleData){
    console.log("---------鼠标事件-----------");
    console.log(singleData);
    var btn_target = $(this);
        if(btn_target.hasClass('disabled')){
            common_ops.alert('正在处理，请不要重复点击！');
            return;
        }
    btn_target.addClass('disabled');
    var getdata = null;
    getdata = function(ip,tm){
    $.ajax({
           url:common_ops.buildUrl("/dbinstall/"),
           type:"POST",
           dataType:"json",
           data:{
                tag:singleData.text,
                ip:ip,
                tm:tm
           },
           success:function (res){
               btn_target.removeClass('disabled');
               if(res.code == 200){
                   common_ops.pop_tab(singleData.text,res.data);
               }
           }
        });
    };
    common_ops.prompt_k(singleData.text,getdata);
}

function db_abs(singleData){
    console.log("---------鼠标事件-----------");
    console.log(singleData);
    var btn_target = $(this);
        if(btn_target.hasClass('disabled')){
            common_ops.alert('正在处理，请不要重复点击！');
            return;
        }
    btn_target.addClass('disabled');
    var getdata = null;
    getdata = function(ip,tbs,tm){
    $.ajax({
           url:common_ops.buildUrl("/dbinstall/"),
           type:"POST",
           dataType:"json",
           data:{
                tag:singleData.text,
                ip:ip,
                tm:tm,
                tbs:tbs
           },
           success:function (res){
               btn_target.removeClass('disabled');
               if(res.code == 200){
                   common_ops.pop_tab(singleData.text,res.data);
               }
           }
        });
    };
    common_ops.prompt_abs(singleData.text,getdata);
}

function sqlserver_check(singleData){
    console.log("---------鼠标事件-----------");
    console.log(singleData);
    var btn_target = $(this);
        if(btn_target.hasClass('disabled')){
            common_ops.alert('正在处理，请不要重复点击！');
            return;
        }
    btn_target.addClass('disabled');
    var getdata = null;
    getdata = function(){
    $.ajax({
           url:common_ops.buildUrl("/dbinstall/"),
           type:"POST",
           dataType:"json",
           data:{
                tag:singleData.text
           },
           success:function (res){
               btn_target.removeClass('disabled');
               if(res.code == 200){
                   common_ops.pop_tab(singleData.text,res.data);
               }
           }
        });
    };
    common_ops.alert(singleData.text,getdata);
}