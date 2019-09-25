var map_plan = new AMap.Map('PlanPath', {
    center: [121.443389,31.02622],
    zoom: 18
});

var southWest = new AMap.LngLat(121.443437,31.025954);
var northEast = new AMap.LngLat(121.443646,31.026363);

var bounds = new AMap.Bounds(southWest, northEast);

var rectangle = new AMap.Rectangle({
    bounds: bounds,
    strokeColor:'red',
    strokeWeight: 6,
    strokeOpacity:0.5,
    strokeDasharray: [30,10],
    // strokeStyle还支持 solid
    strokeStyle: 'dashed',
    fillColor:'blue',
    fillOpacity:0.5,
    cursor:'pointer',
    zIndex:50,
});

rectangle.setMap(map_plan);
// // 缩放地图到合适的视野级别
// map_plan.setFitView([ rectangle ]);

rectangleEditor = new AMap.RectangleEditor(map_plan, rectangle);

rectangleEditor.on('adjust', function(event) {
    log.info('触发事件：adjust')
});

rectangleEditor.on('end', function(event) {
    log.info('触发事件： end');

    var lon = rectangle.Mg.path[0]['lng'];
    var lat = rectangle.Mg.path[0]['lat'];
    var lnglat = new AMap.LngLat(lon, lat);
    pixel = map_plan.lngLatToContainer(lnglat);

    var lon1 = rectangle.Mg.path[2]['lng'];
    var lat1 = rectangle.Mg.path[2]['lat'];
    var lnglat1 = new AMap.LngLat(lon1, lat1);
    pixel1 = map_plan.lngLatToContainer(lnglat1);
    alert(pixel, pixel1);
    // event.target 即为编辑后的矩形对象   rectangle.Mg.path
});

function gen_path() {
    if (window.pathSimplifierIns_plan) {
        pathSimplifierIns_plan.setData([]);
        console.log('reset done');
    }
    var radioValue = $('input:radio[name="func"]:checked').val();
    $.ajax({
        url: "/path_ergodic",
        // type: "POST",
        data: {'w': String(pixel), 'h': String(pixel1), 'method': radioValue},
        dataType: "json",
        success: function (datas) {
            plot_path(datas);
        }
    })
}

function plot_path(datas) {
    var processed_data = [];
    i = 0;
    while (datas[i]) {
        var temp = new AMap.Pixel(datas[i][0], datas[i][1]);
        processed_data[i] = map_plan.containerToLngLat(temp);
        i = i + 1;
    }
    var choice_plan = confirm("是否将该条路径提交之数据库?");
    if (choice_plan === true) {
        $.ajax({
            url: "/save_path",
            // type: "POST",
            data: {'data': String(processed_data)},
            dataType: "text",
            success: function () {
                console.log('save success')
            },
            error: function(e){
                alert(e)
            }
        })
    }

    AMapUI.load(['ui/misc/PathSimplifier'], function(PathSimplifier) {
        initPage(PathSimplifier);
    });
    function initPage(PathSimplifier) {

    var pathSimplifierIns_plan = new PathSimplifier({
    zIndex: 100,
    map: map_plan, //所属的地图实例
    getPath: function(pathData, pathIndex) {
        //返回轨迹数据中的节点坐标信息，[AMap.LngLat, AMap.LngLat...] 或者 [[lng|number,lat|number],...]
        return pathData.path;
    },
    getHoverTitle: function(pathData, pathIndex, pointIndex) {
        //返回鼠标悬停时显示的信息
        if (pointIndex >= 0) {
            //鼠标悬停在某个轨迹节点上
            //鼠标悬停在某个轨迹节点上
            return pathData.name + '，点:' + pointIndex + '/' + pathData.path.length;
        }
        //鼠标悬停在节点之间的连线上
        return pathData.name + '，点数量' + pathData.path.length;
    },
    renderOptions: {
        //轨迹线的样式
        pathLineStyle: {
            strokeStyle: 'red',
            lineWidth: 6,
            dirArrowStyle: true
        }
    }
    });
    window.pathSimplifierIns_plan = pathSimplifierIns_plan;
    pathSimplifierIns_plan.setData([{
        name: '轨迹0',
        path: processed_data
    }]);
    var navg1 = pathSimplifierIns_plan.createPathNavigator(0, //关联第1条轨迹
    {
        loop: true, //循环播放
        speed: 10
    });

    navg1.start();
    }
}

