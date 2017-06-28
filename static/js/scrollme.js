(function ($){

	$(document).ready(function() {
		//hide navbar first
		$('.navscroll').hide();

		//fade-in .navbar
		$(function (){
			$(window).scroll(function (){
				console.log($('.jumbotron').position());
				$(this).scrollTop() > $('.jumbotron').position().top + $('.jumbotron').height() ? $('.navscroll').fadeIn() : $('.navscroll').fadeOut();
			});
		})
	});
}(jQuery));