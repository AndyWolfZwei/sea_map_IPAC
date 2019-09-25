    //创建地图
var map = new AMap.Map('ShowPath', {
    center: [121.443389,31.02622],
    zoom: 18
});
AMapUI.load(['ui/misc/PathSimplifier'], function(PathSimplifier) {
        initPage(PathSimplifier);
    });
function initPage(PathSimplifier) {

    var pathSimplifierIns = new PathSimplifier({
        zIndex: 100,
        map: map,
        getPath: function (pathData, pathIndex) {
            return pathData.path;
        },
        getHoverTitle: function (pathData, pathIndex, pointIndex) {
            if (pointIndex >= 0) {
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
    window.pathSimplifierIns = pathSimplifierIns;
    pathSimplifierIns.setData([{
        name: '轨迹0',
        path: processed_data
    }]);
    var navg = pathSimplifierIns.createPathNavigator(0, //关联第1条轨迹
    {
        loop: true, //循环播放
        speed: 10
    });
    navg.start();
}

function plot_path1(path) {
    var processed_data = [];
    var i =0;
    var path0 = path['paths'];
    while (path0[i]) {
        processed_data[i] = [path0[i][0], path0[i][1]];
        i = i + 1;
    }

    alert('done');
    window.pathSimplifierIns.setData([{
        name: '轨迹0',
        path: processed_data
    }]);
    var navg = window.pathSimplifierIns.createPathNavigator(0, //关联第1条轨迹
    {
        loop: true,
        speed: 10
    });
    navg.start();
}