console.log("inside main.js")




$(document).ready(function() {

  var ctxheight = $('#canvas')[0];
  ctxheight.height = 100;


$("#outputtext").hide();
$("#outputprob").hide();
$("#output").hide();
$("#errortext").hide();
$("#alertdanger").hide();

$('#load').on('click', function() {

    $("#output").hide();
    $("#canvas").hide();
    $("#outputtext").hide();
    $("#outputprob").hide();
    $("#errortext").hide();
    $("#alertdanger").hide();

    var $this = $(this);
    $this.button('loading');
    setTimeout(function() {

    var imageurlone = document.getElementById('imageurl').value;

    if (checkURL(imageurlone)) {

      myFunction();
    }
    else{

      $("#alertdanger").show();
      $("#errortext").show();

    }

    console.log(checkURL(imageurlone))

    function checkURL(imageurlone) {
          return(imageurlone.match(/\.(jpeg|jpg|gif|png)$/) != null);

    }
    $this.button('reset');

   }, 2000);
});



function myFunction() {

    //console.log("the form has beeen submitted");
    console.log("inside myFunction");
    //var imageurlone = $('#imageurl').val();






      //  var imageurlone = 'http://www.homedepot.com/catalog/productImages/1000/a6/a619a055-6979-4b47-b0da-5dfa09d6ca2b_1000.jpg';
    var imageurlone = document.getElementById('imageurl').value;
    var data = {
      'imageurl': imageurlone
    }
    console.log(imageurlone);
    console.log(data)
    console.log("end");

    $.ajax({
              type: "POST",
              url: "/api/v1/classify_image",
              data : JSON.stringify(data, null, '\t'),
              contentType: 'application/json;charset=UTF-8',
              beforeSend: function(){
                 // Show image container


                },
              success: function(results) {

                // var $this = $(this);
                // $this.button('loading');
                //   setTimeout(function() {
                //      $this.button('reset');
                //  }, 8000);
              $("#outputtext").show();
              $("#outputprob").show();
              console.log(results);
              // console.log(typeof(results));
              // JSONObject resultsjson = new JSONObject(results);
              resultsjson = JSON.parse(results)
              predictionkey = Object.keys(resultsjson).reduce((a, b) => resultsjson[a] > resultsjson[b] ? a : b);
              predictionvalue = resultsjson[predictionkey] * 100
              console.log(predictionvalue)
              var probcategory = document.getElementById('probcategory');
              probcategory.innerHTML = predictionkey;
              var probpercentage = document.getElementById('probpercentage');
              probpercentage.innerHTML = predictionvalue;
              // console.log(resultsjson);
              // console.log(typeof(resultsjson));
              var output = document.getElementById('output');
              // results = Object.keys(resultsjson).map((a) => resultsjson[a] * 100);
              // console.log(typeof results)
              // console.log(results)
              var probfaucet = document.getElementById('probfaucet');
              var probhammer = document.getElementById('probhammer');
              var probthermostats = document.getElementById('probthermostats');
              var probflowerpots = document.getElementById('probflowerpots');
              probfaucet.innerHTML = resultsjson['faucet'] * 100;
              probhammer.innerHTML = resultsjson['hammer'] * 100;
              probthermostats.innerHTML = resultsjson['thermostats'] * 100;
              probflowerpots.innerHTML = resultsjson['flowerpots'] * 100;
              var jsonfile = {
                 "jsonarray": [
                 {
                    "name": "faucet",
                    "probability": resultsjson['faucet'] * 100
                 }, {
                    "name": "hammer",
                    "probability": resultsjson['hammer'] * 100
                 }, {
                    "name": "thermostat",
                    "probability": resultsjson['thermostats'] * 100
                 }, {
                    "name": "flowerpot",
                    "probability": resultsjson['flowerpots'] * 100
                 }
                 ]
               }
               var labels = jsonfile.jsonarray.map(function(e) {
	             return e.name;
              	});
              	var data = jsonfile.jsonarray.map(function(e) {
              	   return e.probability;
              	});;
                console.log(data)

              	var ctx = canvas.getContext('2d');

              	var config = {
              	   type: 'line',
              	   data: {
              	      labels: labels,
              	      datasets: [{
              	         label: 'Probability',
              	         data: data,
              	         backgroundColor: 'rgba(0, 119, 204, 0.3)'
              	      }],

                      options: {
                        responsive: true,
                        maintainAspectRatio: false
                      }

              	   }
              	};

              	var chart = new Chart(ctx, config);
                $("#outputtext").show();
                $("#outputprob").show();
                $("#output").show();
                $("#canvas").show();

              },
              complete:function(data){



               },
              error: function(error) {
                  console.log(error)
                  var serverresponse = document.getElementById('serverresponse');
                  serverresponse.innerHTML = error.statusText;
                  var serverstatus = document.getElementById('serverstatus');
                  serverstatus.innerHTML = error.status;
                  $("#alertdanger").show();
              }

            });



}

});
