$('.owl-carousel').owlCarousel({
    loop: true,
    margin: 10,
    nav:true,
    items: 1,
    autoplay:true,
    autoplayTimeout:6000,
    autoplayHoverPause:true,
    responsive:{
      0:{
        items:1
      },
      600: {
        items:1
      },
      1000:{
        items:1
      }
    }
  })