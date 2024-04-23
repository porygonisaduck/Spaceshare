function redirectToPage(url, delay){
    setTimeout(function() {
        window.location.href = url;
    }, delay);
}

document.getElementById("houseListing").addEventListener("submit", function (e) {
  e.preventDefault();
  getListing(e.target);
});

function addListing() {
    var overlay = document.createElement('div');
    overlay.className = 'overlay';
  
    var tempPage = document.createElement('div');
    tempPage.className = 'temp-page';
    tempPage.innerHTML = `
      <i aria-label="exit-listing" class="fa-2x fa-solid fa-angle-left" onclick="closeListing()"></i>
      <h3 style="">Add Listing to Registered Place:</h3>
      <form class="inline" action="" method="" enctype="" id="houseListing">
        <label for="textInput">Listing Headline
        <input type="text" name="headline" required/>
        </label>
        <label for="textInput">Description of Space
        <input type="text" name="description" required/>
        </label>
        <label for="textInput">Item Guidelines
        <input type="text" name="guidlines" required/>
        </label>
        <input type="submit" value="Submit">
      </form>`;
  
    // Append temporary page to overlay
    overlay.appendChild(tempPage);
  
    // Append overlay to body
    document.body.appendChild(overlay);
  }

  function getListing(form) {
    var formData = new FormData(form);

    document.getElementById("all-posts").innerHTML += `
    <div class="post">
        <div class="left-side">
            <h5 class="text-style">Little Village | Chicago</h5>
            <p class="text-style">0.1 miles away</p>
            <p class="text-style">5x10 small backyard patio | apt.
                Non-flammable items please!</p>
        </div>
        <div class="right-side">
            <img class="post-image" src="/uploads/little-village-1800x853.png">
        </div>
    </div>`;
  }
  
  function closeListing() {
    var overlay = document.querySelector('.overlay');
    if (overlay) {
      overlay.remove();
    }
  }


  function sendOffer() {
    var overlay = document.createElement('div');
    overlay.className = 'overlay';
  
    var tempPage = document.createElement('div');
    tempPage.className = 'temp-page';
    tempPage.innerHTML = `
      <i aria-label="exit-listing" class="fa-2x fa-solid fa-angle-left" onclick="closeListing()"></i>
      <h3 style="">Send offer for location:</h3>
      <form class="inline" action="" method="" enctype="" id="">
        <label for="textInput">Offer (in USD)
        <input type="text" name="offer" required/>
        </label>
        <input type="submit" value="Send Offer">
      </form>`;
  
    // Append temporary page to overlay
    overlay.appendChild(tempPage);
  
    // Append overlay to body
    document.body.appendChild(overlay);
  }

  function closeListing() {
    var overlay = document.querySelector('.overlay');
    if (overlay) {
      overlay.remove();
    }
  }