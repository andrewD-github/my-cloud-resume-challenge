// Select the element with the class 'visit-count'
var countOnPage = document.querySelector(".visit-count");

fetch('https://ntayl2xwge.execute-api.ap-southeast-2.amazonaws.com/Prod/updatecount', {
    method: 'PUT'  // Increment the counter in the database
})
    .then(() => {
        // After updating, call the GET endpoint to retrieve the updated count
        return fetch('https://ntayl2xwge.execute-api.ap-southeast-2.amazonaws.com/Prod/viewcount');
    })
    .then(response => response.json())
    .then((data) => {
        // Update the visitor count on the page
        if (countOnPage) {
            countOnPage.innerHTML = data.count;
        } else {
            console.error('Element with class "visit-count" not found.');
        }
    })
    .catch(error => {
        console.error('Error updating or fetching visitor count:', error);
    });

// test code before i added the api call to get the count
/* 
var visitCountStored = localStorage.getItem("visitCount");
if (visitCountStored) { //if we already have a count stored add one to it
  visitCountStored = Number(visitCountStored) + 1; 
  localStorage.setItem("visitCount", visitCountStored);
} else { // else this is the first time so it's 1
  visitCountStored = 1;
  localStorage.setItem("visitCount", 1);
}
CountOnPage.innerHTML = visitCountStored; // Update the HTML counter shown on the web page
*/
