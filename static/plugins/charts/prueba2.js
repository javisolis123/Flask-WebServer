var chartTemperatue;
var chartHumidity;

        function requestData() {
            // Ajax call to get the Data from Flask
            var requests = $.get('/datos');

            var tm = requests.done(function (result) {
                //alarmas
                
                // Temperature
                var seriesTemperature = chartTemperatue.series[0],
                    shiftTemperature = seriesTemperature.data.length > 20;

                // Humidity
                var seriesHumidity = chartHumidity.series[0],
                    shiftHumidity = seriesTemperature.data.length > 20;

                // Add the Point
                // Time Temperature\
                var data1 = [];
                data1.push(result[8]);
                data1.push(result[2]);


                // Add the Point
                // Time Humidity
                var data2 = [];
                data2.push(result[8]);
                data2.push(result[3]);


                chartTemperatue.series[0].addPoint(data1, true, shiftTemperature);
                chartHumidity.series[0].addPoint(data2, true, shiftHumidity);
                
                
               
                
                // call it again after one second
                setTimeout(requestData, 5000);
            });
        }

        $(document).ready(function () {
            // --------------Chart 1 ----------------------------
            chartTemperatue = new Highcharts.Chart({
                chart:
                {
                    renderTo: 'data-temperature',
                    defaultSeriesType: 'spline',
                    events: {
                        load: requestData
                    }
                },
                title:
                {
                    text: 'Potencia de Recepcion Principal'
                },
                xAxis: {
                    type: 'datetime',
                    tickPixelInterval: 150,
                    maxZoom: 20 * 1000
                },
                yAxis: {
                    minPadding: 0.2,
                    maxPadding: 0.2,
                    title: {
                        text: 'Voltaje',
                        margin: 80
                    }
                },
                series: [{
                    color: '#c23d23',
                    lineColor: '#303030',
                    name: 'Potencia Recibida',
                    data: []
                }]
            });
            // --------------Chart 1 Ends - -----------------

            chartHumidity = new Highcharts.Chart({
                chart:
                {
                    renderTo: 'data-humidity',
                    defaultSeriesType: 'spline',
                    events: {
                        load: requestData
                    }
                },
                title:
                {
                    text: 'Potencia de Recepcion Secundaria'
                },
                xAxis: {
                    type: 'datetime',
                    tickPixelInterval: 150,
                    maxZoom: 20 * 1000
                },
                yAxis: {
                    minPadding: 0.2,
                    maxPadding: 0.2,
                    title: {
                        text: 'Voltaje',
                        margin: 80
                    }
                },
                series: [{
                    lineColor: '#1d82b8',
                    name: 'Potencia Recibida',
                    data: []
                }]
            });


        });