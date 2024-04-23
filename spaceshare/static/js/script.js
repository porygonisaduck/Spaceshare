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
      <h3 style="background-color: #c0e4da; padding: 10px;">Add Listing</h3>
      <form class="inline" action="" method="" enctype="" id="houseListing" onsubmit="submitListing(event)">
          <h4 style="text-decoration: underline;">Registered Place:</h4>
          <select name="place" id="placeSelect" required>
              <option value="Southie Apt <3<3">Southie Apt <3<3</option>
              <option value="Workshop Garage">Workshop Garage</option>
              <option value="Auntie Jane's Porch">Auntie Jane's Porch</option>
          </select><br>
          <label for="headlineInput">Listing Headline</label>
          <input type="text" name="headline" id="headlineInput" required/><br>
          <label for="descriptionInput">Description of Space</label>
          <input type="text" name="description" id="descriptionInput" required/><br>
          <label for="guidelinesInput">Item Guidelines</label>
          <input type="text" name="guidelines" id="guidelinesInput" required/><br>
          <label for="durationInput">Duration Guideline</label>
          <input type="text" name="duration" id="durationInput" required/><br>
          <label for="imageInput">Upload Image</label>
          <input type="file" name="image" id="imageInput" accept="image/*" required/><br>
          <input type="submit" value="Submit">
      </form>`;

  // Append temporary page to overlay
  overlay.appendChild(tempPage);

  // Append overlay to body
  document.body.appendChild(overlay);
}



function submitListing(event) {
  event.preventDefault(); // Prevent the form from submitting normally

  // Retrieve input values
  var headline = document.getElementById('headlineInput').value;
  var description = document.getElementById('descriptionInput').value;
  var guidelines = document.getElementById('guidelinesInput').value;
  var image = document.getElementById('imageInput').files[0]; // Get the selected image file

  // Create new post element
  var newPost = document.createElement('div');
  newPost.className = 'post';
  newPost.innerHTML = `
      <div class="left-side">
          <h2 class="italic-text">| Southie Apt. <3<3</h2>
          <h3 class="text-style">${headline}</h3>
          <p class="description text-style">${description}</p>
          <p class="guidelines text-style">${guidelines}</p>
      </div>
      <div class="right-side">
          <img class="post-image" src="${URL.createObjectURL(image)}" alt="Listing Image">
      </div>
  `;

  // Set background color to indicate it's your listing
  newPost.style.backgroundColor = '#c0e4da'; // Light teal background color

  // Get the container where posts are stored
  var allPostsContainer = document.getElementById('all-posts');

  // Get the first post in the container (if any)
  var firstPost = allPostsContainer.firstChild;

  // Insert the new post before the first post (if it exists), otherwise append it to the container
  if (firstPost) {
      // allPostsContainer.insertBefore(newPost, firstPost);
      allPostsContainer.appendChild(newPost);

  } else {
    allPostsContainer.appendChild(newPost);
  }

  // Close the overlay
  closeListing();

  // Append to "southie-apt" id, of the format:
    // // Append additional information to "southie-apt"
    var southieApt = document.getElementById("southie-apt");
    var additionalInfo = document.createElement('div');
    additionalInfo.className = 'left-side';
    additionalInfo.innerHTML = `
        <p class="italic-text">> Pending </p>
        <p class="italic-text">  +1 (000) 000-0000 </p>
    `;
    southieApt.appendChild(additionalInfo);
    // var durationInfo = document.createElement('div');
    // durationInfo.className = 'right-side';
    // durationInfo.textContent = duration + ' days';
    // southieApt.appendChild(durationInfo);
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

  function sendOffer(headline, location, distance, description, recommendedDuration) {
    var overlay = document.createElement('div');
    overlay.className = 'overlay';
  
    var tempPage = document.createElement('div');
    tempPage.className = 'temp-page';
    tempPage.innerHTML = `
      <i aria-label="exit-listing" class="fa-2x fa-solid fa-angle-left" onclick="closeListing()"></i>
      <h3 style="">Send offer for location:</h3>
      <p><strong>${headline}</strong></p>
      <p>${location}</p>
      <p>${distance}</p>
      <p><strong>Sharer Description</strong>: ${description}</p>
      <p><strong>Recommended Duration</strong>: ${recommendedDuration}</p>
      <form class="inline" action="" method="" enctype="" id="">
        <label for="offerInput">Offer (in USD)</label>
        <input type="text" name="offer" id="offerInput" required/>
        <label for="durationInput">Duration</label>
        <input type="text" name="duration" id="durationInput" required/>
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