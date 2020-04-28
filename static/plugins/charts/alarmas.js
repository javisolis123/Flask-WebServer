
var controlador = '/datos';

setInterval(function () {

    $.ajax({url: controlador,
                 type:"POST",
                 data:{},
                 success:function(respuesta){     
                  if(respuesta[7]>0){
                      
                      $("#alarmas").html(respuesta[7]);
                  }
                     //var registros =  JSON.parse(respuesta);
                     var temp = Number(respuesta[0]);
      var point = chart.series[0].points[0],
          newVal,

      newVal = temp;
      

      point.update(newVal);
    
              }
                         
          });
  }, 1000);