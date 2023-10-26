$(document).ready(function() {

    if ($('.bbb_slider').length) {
        var trendsSlider = $('.bbb_slider');
        trendsSlider.owlCarousel({

            loop: false,
            margin: 10,
            nav: false,
            dots: false,
            autoplayHoverPause: true,
            autoplay: false,
            responsive: {
                0: {
                    items: 1
                },
                575: {
                    items: 2
                },
                991: {
                    items: 3
                },
                1371: {
                    items: 4
                }
            }
        });

        trendsSlider.on('click', '.bbb_fav', function(ev) {
            $(ev.target).toggleClass('active');
        });

        if ($('.bbb_prev').length) {
            var prev = $('.bbb_prev');
            prev.on('click', function() {
                trendsSlider.trigger('prev.owl.carousel');
            });
        }

        if ($('.bbb_next').length) {
            var next = $('.bbb_next');
            next.on('click', function() {
                trendsSlider.trigger('next.owl.carousel');
            });
        }
    }

    if ($('.bbb_deals_slider').length) {
        var bbb_dealsSlider = $('.bbb_deals_slider');
        bbb_dealsSlider.owlCarousel({
            items: 1,
            loop: false,
            navClass: ['bbb_deals_slider_prev', 'bbb_deals_slider_next'],
            nav: false,
            dots: false,
            smartSpeed: 1200,
            margin: 30,
            autoplay: false,
            autoplayTimeout: 5000
        });

        if ($('.bbb_deals_slider_prev').length) {
            var prev = $('.bbb_deals_slider_prev');
            prev.on('click', function() {
                bbb_dealsSlider.trigger('prev.owl.carousel');
            });
        }

        if ($('.bbb_deals_slider_next').length) {
            var next = $('.bbb_deals_slider_next');
            next.on('click', function() {
                bbb_dealsSlider.trigger('next.owl.carousel');
            });
        }
    }

    if ($('.bbb_deals_timer_box').length) {
        var timers = $('.bbb_deals_timer_box');
        timers.each(function() {
            var timer = $(this);

            var targetTime;
            var target_date;

            // Add a date to data-target-time of the .bbb_deals_timer_box
            // Format: "Feb 17, 2018"
            if (timer.data('target-time') !== "") {
                targetTime = timer.data('target-time');
                target_date = new Date(targetTime).getTime();
            } else {
                var date = new Date();
                date.setDate(date.getDate() + 2);
                target_date = date.getTime();
            }

            // variables for time units
            var days, hours, minutes, seconds;

            var h = timer.find('.bbb_deals_timer_hr');
            var m = timer.find('.bbb_deals_timer_min');
            var s = timer.find('.bbb_deals_timer_sec');

            setInterval(function() {
                // find the amount of "seconds" between now and target
                var current_date = new Date().getTime();
                var seconds_left = (target_date - current_date) / 1000;
                console.log(seconds_left);

                // do some time calculations
                days = parseInt(seconds_left / 86400);
                seconds_left = seconds_left % 86400;

                hours = parseInt(seconds_left / 3600);
                hours = hours + days * 24;
                seconds_left = seconds_left % 3600;

                minutes = parseInt(seconds_left / 60);
                seconds = parseInt(seconds_left % 60);

                if (hours.toString().length < 2) {
                    hours = "0" + hours;
                }
                if (minutes.toString().length < 2) {
                    minutes = "0" + minutes;
                }
                if (seconds.toString().length < 2) {
                    seconds = "0" + seconds;
                }

                // display results
                h.text(hours);
                m.text(minutes);
                s.text(seconds);

            }, 1000);
        });
    }
    // AGREGANDO CLASE ACTIVE AL PRIMER ENLACE ====================
	$('.category_list .category_item[category="all"]').addClass('ct_item-active');

	// FILTRANDO PRODUCTOS  ============================================

	$('.category_item').click(function(){
		var catProduct = $(this).attr('category');
		console.log(catProduct);

		// AGREGANDO CLASE ACTIVE AL ENLACE SELECCIONADO
		$('.category_item').removeClass('ct_item-active');
		$(this).addClass('ct_item-active');

		// OCULTANDO PRODUCTOS =========================
		$('.product-item').css('transform', 'scale(0)');
		function hideProduct(){
			$('.product-item').hide();
		} setTimeout(hideProduct,400);

		// MOSTRANDO PRODUCTOS =========================
		function showProduct(){
			$('.product-item[category="'+catProduct+'"]').show();
			$('.product-item[category="'+catProduct+'"]').css('transform', 'scale(1)');
		} setTimeout(showProduct,400);
	});

	// MOSTRANDO TODOS LOS PRODUCTOS =======================

	$('.category_item[category="all"]').click(function(){
		function showAll(){
			$('.product-item').show();
			$('.product-item').css('transform', 'scale(1)');
		} setTimeout(showAll,400);
	});
});