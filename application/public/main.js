$(function(){
	
	//smoothie 

	var smoothie=new SmoothieChart({
		timestampFormatter:SmoothieChart.timeFormatter
	});


	var socket=io();


	smoothie.streamTo(document.getElementById("StockChart"),1000);


	var line1=new TimeSeries();

	smoothie.addTimeSeries(line1,{
		lineWidth:3
	});


	//when server emits 'data', updata UI
	socket.on('data',function(data){
		console.log(data);
		parsed=JSON.parse(data)
		line1.append(Math.trunc(parsed['timestamp']*1000),parsed['average'])
	});
});