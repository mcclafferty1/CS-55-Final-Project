$( document ).ready(function() {
	$.ajax({
    	type: 'GET',
    	url: 'industry_sentiment',
		dataType: 'json',
		success: function (data){
		    var sentiment_text = "Sentiment: ";
	  	$( "#tech-sentiment" ).html( sentiment_text + data['Tech'] );
	  	//$( "#tech-sentiment" ).html( "Stuff" );

	  	$( "#finance-sentiment" ).html( data );
	  	$( "#ag-sentiment" ).html( data );
	  	$( "#consumer-sentiment" ).html( data );
	  	$( "#energy-sentiment" ).html( sentiment_text + data['Energy'] );
	  	$( "#automobile-sentiment" ).html( sentiment_text + data['Auto'] );
	  	$( "#re-sentiment" ).html( data );
	  	$( "#pharma-sentiment" ).html( data );
		 }
    });

	$.ajax({
    	type: 'GET',
    	url: 'https://api.us-east.discovery.watson.cloud.ibm.com/instances/7e96e162-cf60-4640-8883-e2f6ab8cb9e3/v1/environments/system/collections/news-en/query?version=2019-04-30&query=enriched_text.entities.text:stock%20market',
		dataType: 'json',
    	headers: {
		    "Authorization" : "Basic " + btoa("apikey:vTWFnFl3TDWpVX1Ha4EnQRyurIHObQuIcU3Xykldpnhy")
		},
		success: function (data){
		    $('#news-1').html('<a target="_blank" href="'+ data.results[0].url +'">'+ data.results[0].title +'</a>');
		    $('#news-2').html('<a target="_blank" href="'+ data.results[1].url +'">'+ data.results[1].title +'</a>');
		    $('#news-3').html('<a target="_blank" href="'+ data.results[2].url +'">'+ data.results[2].title +'</a>');
		    $('#news-4').html('<a target="_blank" href="'+ data.results[3].url +'">'+ data.results[3].title +'</a>');
		    $('#news-5').html('<a target="_blank" href="'+ data.results[4].url +'">'+ data.results[4].title +'</a>');
		    $('#news-6').html('<a target="_blank" href="'+ data.results[5].url +'">'+ data.results[5].title +'</a>');
		    $('#news-7').html('<a target="_blank" href="'+ data.results[6].url +'">'+ data.results[6].title +'</a>');
		  }
		//crossDomain: true,
   		//dataType: 'jsonp',
    });

    $.ajax({
    	type: 'GET',
    	url: 'https://api.us-east.discovery.watson.cloud.ibm.com/instances/7e96e162-cf60-4640-8883-e2f6ab8cb9e3/v1/environments/system/collections/news-en/query?version=2019-04-30&query=enriched_text.entities.text:AAPL',
		dataType: 'json',
    	headers: {
		    "Authorization" : "Basic " + btoa("apikey:vTWFnFl3TDWpVX1Ha4EnQRyurIHObQuIcU3Xykldpnhy")
		},
		success: function (data){
		    $('#stock-news-1').html('<a target="_blank" href="'+ data.results[0].url +'">'+ data.results[0].title +'</a>');
		    $('#stock-news-2').html('<a target="_blank" href="'+ data.results[1].url +'">'+ data.results[1].title +'</a>');
		    $('#stock-news-3').html('<a target="_blank" href="'+ data.results[2].url +'">'+ data.results[2].title +'</a>');
		  }
		//crossDomain: true,
   		//dataType: 'jsonp',
    });
});