var map1 = new AMap.Map('DrawPath', {
    center: [121.441216,31.025492],
    zoom: 18,
});
map1.plugin(["AMap.MouseTool"]);
var mouseTool = new AMap.MouseTool(map1);   //在地图中添加MouseTool插件

function start_edit(){
    mouseTool.polyline();
    window.moustTool = mouseTool;
}
function end_edit(){
    if(window.moustTool){
        moustTool.close(true);
    }
}

AMap.event.addListener( window.mouseTool,'draw',function(e){
    var choice=confirm("是否将该条路径提交之数据库?");
    if(choice === true){
        $.ajax({
        url: "/save_path",
        data: {'path': String(e.obj.getPath())},
        dataType: "text",
        success: function (datas) {
            console.log('ok');},
        error: function (e) {
            console.log('failed');}
        })
    }
});
