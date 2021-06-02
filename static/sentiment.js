//This code is all custom
//This code is what loads the industry sentiment values in the industry sentiment section, and pulls news sources for the stock market and individual stocks
$( document ).ready(function() {
	// Pulls industry sentiment data from the server
	$.ajax({
    	type: 'GET',
    	url: 'industry_sentiment',
		dataType: 'json',
		success: function (data){
		// append the industry sentiments to the home page
		    var sentiment_text = "Sentiment: ";
	  	$( "#tech-sentiment" ).html( sentiment_text + data['Tech'].toFixed(1) );
	  	$( "#finance-sentiment" ).html( sentiment_text + data['Finance'].toFixed(1) );
	  	$( "#ag-sentiment" ).html( sentiment_text + data['Tech'].toFixed(1) );
	  	$( "#cannabis-sentiment" ).html( sentiment_text + data['Cannabis'].toFixed(1) );
	  	$( "#energy-sentiment" ).html( sentiment_text + data['Energy'].toFixed(1) );
	  	$( "#automobile-sentiment" ).html( sentiment_text + data['Auto'].toFixed(1) );
	  	$( "#re-sentiment" ).html( sentiment_text + data['Real Estate'].toFixed(1) );
	  	$( "#pharma-sentiment" ).html( sentiment_text + data['Pharma'].toFixed(1) );
		 }
    });

	// Pulls 8 news articles about the overall stock market and displays it on the dashboard
	$.ajax({
    	type: 'GET',
    	url: 'https://api.us-south.discovery.watson.cloud.ibm.com/instances/d19e700b-3209-4869-a8bb-279a7b7c4e8a/v1/environments/system/collections/news-en/query?version=2019-04-30&query=enriched_text.entities.text:stock%20market',
		dataType: 'json',
    	headers: {
		    "Authorization" : "Basic " + btoa("apikey:a-pugZwx81CeazpgllKNPgfWxIXBYGgpJj-qsIq4MsVb")
		},
		success: function (data){
			// append links to the news articles on the dashboard
		    $('#news-1').html('<a target="_blank" href="'+ data.results[0].url +'">'+ data.results[0].title +'</a>');
		    $('#news-2').html('<a target="_blank" href="'+ data.results[1].url +'">'+ data.results[1].title +'</a>');
		    $('#news-3').html('<a target="_blank" href="'+ data.results[2].url +'">'+ data.results[2].title +'</a>');
		    $('#news-4').html('<a target="_blank" href="'+ data.results[3].url +'">'+ data.results[3].title +'</a>');
		    $('#news-5').html('<a target="_blank" href="'+ data.results[4].url +'">'+ data.results[4].title +'</a>');
		    $('#news-6').html('<a target="_blank" href="'+ data.results[5].url +'">'+ data.results[5].title +'</a>');
		    $('#news-7').html('<a target="_blank" href="'+ data.results[6].url +'">'+ data.results[6].title +'</a>');
		  }
    });

	// Pulls 3 news articles for apple and displays them at the bottom of the page when the page is initially loaded
    $.ajax({
    	type: 'GET',
    	url: 'https://api.us-south.discovery.watson.cloud.ibm.com/instances/d19e700b-3209-4869-a8bb-279a7b7c4e8a/v1/environments/system/collections/news-en/query?version=2019-04-30&query=enriched_text.entities.text:AAPL',
		dataType: 'json',
    	headers: {
		    "Authorization" : "Basic " + btoa("apikey:a-pugZwx81CeazpgllKNPgfWxIXBYGgpJj-qsIq4MsVb")
		},
		success: function (data){
			// append links to the stock's news articles at the bottom of the page
		    $('#stock-news-1').html('<a target="_blank" href="'+ data.results[0].url +'">'+ data.results[0].title +'</a>');
		    $('#stock-news-2').html('<a target="_blank" href="'+ data.results[1].url +'">'+ data.results[1].title +'</a>');
		    $('#stock-news-3').html('<a target="_blank" href="'+ data.results[2].url +'">'+ data.results[2].title +'</a>');
		  }
    });
});