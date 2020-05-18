
var controlador = '/datos';

setInterval(function () {

    $.ajax({url: controlador,
                 type:"POST",
                 data:{},
                 success:function(respuesta){     
                  if(respuesta[7]>0){
                      
                      $("#alarmas").html(respuesta[7]);
                  }else{
                    $("#alarmas").html('');
                  }
                    
    
              }
                         
          });
  }, 1000);