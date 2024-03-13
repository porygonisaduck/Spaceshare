function redirectToPage(url, delay){
    setTimeout(function() {
        window.location.href = url;
    }, delay);
}

function addListing() {
    var overlay = document.createElement('div');
    overlay.className = 'overlay';
  
    var tempPage = document.createElement('div');
    tempPage.className = 'temp-page';
    tempPage.innerHTML = `
      <i aria-label="exit-listing" class="fa-2x fa-solid fa-angle-left"></i>
      <h3>Add Listing to Registered Place:</h3>
      <i aria-label="map-pin" class="fa-2x fa-solid fa-map-pin"></i>
      <form class="inline" action="" method="" enctype="">
        <label for="textInput">Listing Headline</label>
        <input type="text" name="headline" required/>
        <label for="textInput">Description of Space</label>
        <input type="text" name="description" required/>
        <label for="textInput">Item Guidelines</label>
        <input type="text" name="guidlines" required/>
      </form>
      
      <button onclick="closeListing()">Close</button>`;
  
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
