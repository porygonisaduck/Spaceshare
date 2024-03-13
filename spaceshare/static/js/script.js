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
    tempPage.innerHTML = '<h2>Temporary Page</h2><p>This is a temporary page.</p><button onclick="closeListing()">Close</button>';
  
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
