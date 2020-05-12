var TDHeatmap = L.TimeDimension.Layer.extend({

    initialize: function (data, options) {
        var heatmapCfg = {
            radius: 15,
            maxOpacity: 1.,
            scaleRadius: false,
            useLocalExtrema: false,
            latField: 'lat',
            lngField: 'lng',
            valueField: 'count',
            defaultWeight: 1,
        };
        heatmapCfg = $.extend({}, heatmapCfg, options.heatmapOptions || {});
        var layer = new HeatmapOverlay(heatmapCfg);
        L.TimeDimension.Layer.prototype.initialize.call(this, layer, options);
        this._currentLoadedTime = 0;
        this._currentTimeData = {
            data: []
        };
        this.data = data;
        this.defaultWeight = heatmapCfg.defaultWeight || 1;
    },
    onAdd: function (map) {
        L.TimeDimension.Layer.prototype.onAdd.call(this, map);
        map.addLayer(this._baseLayer);
        if (this._timeDimension) {
            this._getDataForTime(this._timeDimension.getCurrentTime());
        }
    },
    _onNewTimeLoading: function (ev) {
        this._getDataForTime(ev.time);
        return;
    },
    isReady: function (time) {
        return (this._currentLoadedTime == time);
    },
    _update: function () {
        this._baseLayer.setData(this._currentTimeData);
        return true;
    },
    _getDataForTime: function (time) {
        delete this._currentTimeData.data;
        this._currentTimeData.data = [];
        var data = this.data[time - 1];
        for (var i = 0; i < data.length; i++) {
            this._currentTimeData.data.push({
                lat: data[i][0],
                lng: data[i][1],
                count: data[i].length > 2 ? data[i][2] : this.defaultWeight
            });
        }
        this._currentLoadedTime = time;
        if (this._timeDimension && time == this._timeDimension.getCurrentTime() && !this._timeDimension.isLoading()) {
            this._update();
        }
        this.fire('timeload', {
            time: time
        });
    }
});

L.Control.TimeDimensionCustom = L.Control.TimeDimension.extend({
    initialize: function (index, options) {
        var playerOptions = {
            buffer: 1,
            minBufferReady: -1
        };
        options.playerOptions = $.extend({}, playerOptions, options.playerOptions || {});
        L.Control.TimeDimension.prototype.initialize.call(this, options);
        this.index = index;
    },
    _getDisplayDateFormat: function (date) {
        return this.index[date.getTime() - 1];
    }
});