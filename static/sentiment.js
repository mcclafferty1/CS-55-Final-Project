$( document ).ready(function() {
    $.get( "industry_sentiment", function( data ) {
	  $( "#tech-sentiment" ).html( data );
	  $( "#finance-sentiment" ).html( data );
	  $( "#ag-sentiment" ).html( data );
	  $( "#consumer-sentiment" ).html( data );
	  $( "#energy-sentiment" ).html( data );
	  $( "#automobile-sentiment" ).html( data );
	  $( "#re-sentiment" ).html( data );
	  $( "#pharma-sentiment" ).html( data );
	  alert( "Load was performed." );
	});
});