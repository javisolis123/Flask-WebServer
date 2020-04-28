Highcharts.chart('gauge1', {

    chart: {
        type: 'gauge',
        plotBackgroundColor: null,
        plotBackgroundImage: null,
        plotBorderWidth: 0,
        plotShadow: false
    },

    title: {
        text: 'Temperatura'
    },

    pane: {
        startAngle: -150,
        endAngle: 150,
        background: [{
            backgroundColor: {
                linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                stops: [
                    [0, '#FFF'],
                    [1, '#333']
                ]
            },
            borderWidth: 0,
            outerRadius: '109%'
        }, {
            backgroundColor: {
                linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                stops: [
                    [0, '#333'],
                    [1, '#FFF']
                ]
            },
            borderWidth: 1,
            outerRadius: '107%'
        }, {
            // default background
        }, {
            backgroundColor: '#DDD',
            borderWidth: 0,
            outerRadius: '105%',
            innerRadius: '103%'
        }]
    },

    // the value axis
    yAxis: {
        min: 0,
        max: 100,

        minorTickInterval: 'auto',
        minorTickWidth: 1,
        minorTickLength: 10,
        minorTickPosition: 'inside',
        minorTickColor: '#666',

        tickPixelInterval: 30,
        tickWidth: 2,
        tickPosition: 'inside',
        tickLength: 10,
        tickColor: '#666',
        labels: {
            step: 2,
            rotation: 'auto'
        },
        title: {
            text: '°C'
        },
        plotBands: [{
            from: 12,
            to: 40,
            color: '#55BF3B' // green
        }, {
            from: 0,
            to: 12,
            color: '#DDDF0D' // yellow
        }, {
            from: 40,
            to: 100,
            color: '#DF5353' // red
        }]
    },

    series: [{
        name: 'Temperatura',
        data: [0],
        tooltip: {
            valueSuffix: ' °C'
        }
    }]

},
// Add some life
function (chart) {
    if (!chart.renderer.forExport) {
      
      var controlador = '/datos';
      
        setInterval(function () {

          $.ajax({url: controlador,
                       type:"POST",
                       data:{},
                       success:function(respuesta){     
                          
                           //var registros =  JSON.parse(respuesta);
                           var temp = Number(respuesta[0]);
            var point = chart.series[0].points[0],
                newVal,

            newVal = temp;
            

            point.update(newVal);
          
                    }
                               
                });
        }, 5000);
    }
});

Highcharts.chart('gauge2', {

    chart: {
        type: 'gauge',
        plotBackgroundColor: null,
        plotBackgroundImage: null,
        plotBorderWidth: 0,
        plotShadow: false
    },

    title: {
        text: 'Humedad'
    },

    pane: {
        startAngle: -150,
        endAngle: 150,
        background: [{
            backgroundColor: {
                linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                stops: [
                    [0, '#FFF'],
                    [1, '#333']
                ]
            },
            borderWidth: 0,
            outerRadius: '109%'
        }, {
            backgroundColor: {
                linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                stops: [
                    [0, '#333'],
                    [1, '#FFF']
                ]
            },
            borderWidth: 1,
            outerRadius: '107%'
        }, {
            // default background
        }, {
            backgroundColor: '#DDD',
            borderWidth: 0,
            outerRadius: '105%',
            innerRadius: '103%'
        }]
    },

    // the value axis
    yAxis: {
        min: 0,
        max: 200,

        minorTickInterval: 'auto',
        minorTickWidth: 1,
        minorTickLength: 10,
        minorTickPosition: 'inside',
        minorTickColor: '#666',

        tickPixelInterval: 30,
        tickWidth: 2,
        tickPosition: 'inside',
        tickLength: 10,
        tickColor: '#666',
        labels: {
            step: 2,
            rotation: 'auto'
        },
        title: {
            text: '%'
        },
        plotBands: [{
            from: 0,
            to: 120,
            color: '#55BF3B' // green
        }, {
            from: 120,
            to: 160,
            color: '#DDDF0D' // yellow
        }, {
            from: 160,
            to: 200,
            color: '#DF5353' // red
        }]
    },

    series: [{
        name: 'Humedad',
        data: [0],
        tooltip: {
            valueSuffix: ' %'
        }
    }]

},
// Add some life
function (chart) {
    if (!chart.renderer.forExport) {
      
      var controlador = '/datos';
       
        setInterval(function () {

          $.ajax({url: controlador,
                       type:"POST",
                       data:{},
                       success:function(respuesta){     
                           
                           //var registros =  JSON.parse(respuesta);
                           var temp = Number(respuesta[1]);
            var point = chart.series[0].points[0],
                newVal,

            newVal = temp;
            

            point.update(newVal);
          
                    }
                               
                });
        }, 5000);
    }
});

//gabinete

Highcharts.chart('gauge3', {

    chart: {
        type: 'gauge',
        plotBackgroundColor: null,
        plotBackgroundImage: null,
        plotBorderWidth: 0,
        plotShadow: false
    },

    title: {
        text: 'Temperatura Gabinete'
    },

    pane: {
        startAngle: -150,
        endAngle: 150,
        background: [{
            backgroundColor: {
                linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                stops: [
                    [0, '#FFF'],
                    [1, '#333']
                ]
            },
            borderWidth: 0,
            outerRadius: '109%'
        }, {
            backgroundColor: {
                linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                stops: [
                    [0, '#333'],
                    [1, '#FFF']
                ]
            },
            borderWidth: 1,
            outerRadius: '107%'
        }, {
            // default background
        }, {
            backgroundColor: '#DDD',
            borderWidth: 0,
            outerRadius: '105%',
            innerRadius: '103%'
        }]
    },

    // the value axis
    yAxis: {
        min: 0,
        max: 200,

        minorTickInterval: 'auto',
        minorTickWidth: 1,
        minorTickLength: 10,
        minorTickPosition: 'inside',
        minorTickColor: '#666',

        tickPixelInterval: 30,
        tickWidth: 2,
        tickPosition: 'inside',
        tickLength: 10,
        tickColor: '#666',
        labels: {
            step: 2,
            rotation: 'auto'
        },
        title: {
            text: '°C'
        },
        plotBands: [{
            from: 0,
            to: 120,
            color: '#55BF3B' // green
        }, {
            from: 120,
            to: 160,
            color: '#DDDF0D' // yellow
        }, {
            from: 160,
            to: 200,
            color: '#DF5353' // red
        }]
    },

    series: [{
        name: 'Temperatura',
        data: [0],
        tooltip: {
            valueSuffix: ' °C'
        }
    }]

},
// Add some life
function (chart) {
    if (!chart.renderer.forExport) {
      
      var controlador = '/datos';
       
        setInterval(function () {

          $.ajax({url: controlador,
                       type:"POST",
                       data:{},
                       success:function(respuesta){     
                           
                           //6  viene de gabinete
                           var temp = Number(respuesta[6]);
            var point = chart.series[0].points[0],
                newVal,

            newVal = temp;
            

            point.update(newVal);
          
                    }
                               
                });
        }, 5000);
    }
});


//Canal 1

Highcharts.chart('gauge4', {

    chart: {
        type: 'gauge',
        plotBackgroundColor: null,
        plotBackgroundImage: null,
        plotBorderWidth: 0,
        plotShadow: false
    },

    title: {
        text: 'Potencia Canal 1'
    },

    pane: {
        startAngle: -150,
        endAngle: 150,
        background: [{
            backgroundColor: {
                linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                stops: [
                    [0, '#FFF'],
                    [1, '#333']
                ]
            },
            borderWidth: 0,
            outerRadius: '109%'
        }, {
            backgroundColor: {
                linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                stops: [
                    [0, '#333'],
                    [1, '#FFF']
                ]
            },
            borderWidth: 1,
            outerRadius: '107%'
        }, {
            // default background
        }, {
            backgroundColor: '#DDD',
            borderWidth: 0,
            outerRadius: '105%',
            innerRadius: '103%'
        }]
    },

    // the value axis
    yAxis: {
        min: 0,
        max: 5,

        minorTickInterval: 'auto',
        minorTickWidth: 1,
        minorTickLength: 10,
        minorTickPosition: 'inside',
        minorTickColor: '#666',

        tickPixelInterval: 30,
        tickWidth: 2,
        tickPosition: 'inside',
        tickLength: 10,
        tickColor: '#666',
        labels: {
            step: 2,
            rotation: 'auto'
        },
        title: {
            text: 'V'
        },
        plotBands: [{
            from: 2,
            to: 4,
            color: '#55BF3B' // green
        }, {
            from: 0,
            to: 2,
            color: '#DDDF0D' // yellow
        }, {
            from: 4,
            to: 5,
            color: '#DF5353' // red
        }]
    },

    series: [{
        name: 'Potencia',
        data: [0],
        tooltip: {
            valueSuffix: ' V'
        }
    }]

},
// Add some life
function (chart) {
    if (!chart.renderer.forExport) {
      
      var controlador = '/datos';
      
        setInterval(function () {

          $.ajax({url: controlador,
                       type:"POST",
                       data:{},
                       success:function(respuesta){     
                           
                           //2  viene de canal 1
                           var temp = Number(respuesta[2]);
            var point = chart.series[0].points[0],
                newVal,

            newVal = temp;
            

            point.update(newVal);
          
                    }
                               
                });
        }, 5000);
    }
});



//Canal 2

Highcharts.chart('gauge5', {

    chart: {
        type: 'gauge',
        plotBackgroundColor: null,
        plotBackgroundImage: null,
        plotBorderWidth: 0,
        plotShadow: false
    },

    title: {
        text: 'Potencia Canal 2'
    },

    pane: {
        startAngle: -150,
        endAngle: 150,
        background: [{
            backgroundColor: {
                linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                stops: [
                    [0, '#FFF'],
                    [1, '#333']
                ]
            },
            borderWidth: 0,
            outerRadius: '109%'
        }, {
            backgroundColor: {
                linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1 },
                stops: [
                    [0, '#333'],
                    [1, '#FFF']
                ]
            },
            borderWidth: 1,
            outerRadius: '107%'
        }, {
            // default background
        }, {
            backgroundColor: '#DDD',
            borderWidth: 0,
            outerRadius: '105%',
            innerRadius: '103%'
        }]
    },

    // the value axis
    yAxis: {
        min: 0,
        max: 5,

        minorTickInterval: 'auto',
        minorTickWidth: 1,
        minorTickLength: 10,
        minorTickPosition: 'inside',
        minorTickColor: '#666',

        tickPixelInterval: 30,
        tickWidth: 2,
        tickPosition: 'inside',
        tickLength: 10,
        tickColor: '#666',
        labels: {
            step: 2,
            rotation: 'auto'
        },
        title: {
            text: 'V'
        },
        plotBands: [{
            from: 2,
            to: 4,
            color: '#55BF3B' // green
        }, {
            from: 0,
            to: 2,
            color: '#DDDF0D' // yellow
        }, {
            from: 4,
            to: 5,
            color: '#DF5353' // red
        }]
    },

    series: [{
        name: 'Potencia',
        data: [0],
        tooltip: {
            valueSuffix: ' V'
        }
    }]

},
// Add some life
function (chart) {
    if (!chart.renderer.forExport) {
      
      var controlador = '/datos';
      
        setInterval(function () {

          $.ajax({url: controlador,
                       type:"POST",
                       data:{},
                       success:function(respuesta){     
                           
                           //3  viene de canal 2
                           var temp = Number(respuesta[3]);
            var point = chart.series[0].points[0],
                newVal,

            newVal = temp;
            

            point.update(newVal);
          
                    }
                               
                });
        }, 5000);
    }
});