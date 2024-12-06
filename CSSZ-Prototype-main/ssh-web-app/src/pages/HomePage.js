import React, { useEffect } from 'react';

const HomePage = () => {
  useEffect(() => {
    if (window.$) {
      const $ = window.$;

      $(".owl-carousel-testimonials").owlCarousel({
        loop: true,
        margin: 20,
        nav: true,
        navText: ["<i class='fa fa-angle-left'></i>", "<i class='fa fa-angle-right'></i>"],
        dots: false,
        items: 1,
        responsive: {
          0: { items: 1 },
          768: { items: 2 },
          992: { items: 3 },
          1200: { items: 4 },
        },
      });
      return () => {
        $(".owl-carousel-testimonials").trigger("destroy.owl.carousel");
      };
    } else {
      console.error("jQuery is not loaded");
    }
  }, []);

  return (
    <div className="container-fluid mainContainer">
      <div className="row">
        <h1 className="title_features">Welcome to SSH Smart Homes!</h1>
      </div>

      <div className="row">
        <h1 className="subHeading_style title_features_position">Possible content to add</h1>
      </div>

      <div className="row">
        <h1 className="subHeading_style title_features_position">Customer Testimonials</h1>
      </div>

      <div className="row">
        <div className="container owlTestimonialsContainer">
          <div className="owl-carousel owl-theme owl-carousel-testimonials">
            <div className="item">
              <div className="container center">
                <div className="card-body">
                  <blockquote>
                    <p>"This app has made it so easy to find recipes that fit my dietary needs. The personalized recipe suggestions are spot on, making meal planning less of a chore and more of a joy "</p>
                    <p>- Alice Brown</p>
                  </blockquote>
                </div>
              </div>
            </div>
            <div className="item">
              <div className="container center">
                <div className="card-body">
                  <blockquote>
                    <p>"The ability to set up a vegan dietary profile and get personalized recipe recommendations has made my dietary journey exciting and delicious! Highly recommend SSH to all users."</p>
                    <p>- David Clark</p>
                  </blockquote>
                </div>
              </div>
            </div>
            <div className="item">
              <div className="container center">
                <div className="card-body">
                  <blockquote>
                    <p>"The personalized recipes based on my dietary preferences save me so much time. I can prepare quick, healthy meals without having to scour through hundreds of recipes online."</p>
                    <p>- Emma Lewis</p>
                  </blockquote>
                </div>
              </div>
            </div>
            <div className="item">
              <div className="container center">
                <div className="card-body">
                  <blockquote>
                    <p>"I've tried many recipe apps, but none compare to the personalization that this one offers. Setting up my dietary profile was so easy  and now I receive recipes that perfectly match my nutritional needs"</p>
                    <p>- Sarah Johnson</p>
                  </blockquote>
                </div>
              </div>
            </div>
            <div className="item">
              <div className="container center">
                <div className="card-body">
                  <blockquote>
                    <p>"The notification feature is amazing. I never had any food waste by the end of the week as the App always prompts me with recipes to use ingredients that are nearing their expiration dates."</p>
                    <footer>- James Wilson</footer>
                  </blockquote>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HomePage;
