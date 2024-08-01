$foo = array("h1", "h2", "label")
$($foo).each(function(index) {
$(this).delay(5000*index).queue(function() { 
$(this).css('font-family', 'fantasy');
})
});