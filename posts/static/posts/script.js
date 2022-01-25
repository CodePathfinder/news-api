document.addEventListener('DOMContentLoaded', function () {

  document.querySelectorAll('.vote-bttn').forEach(button => {
    button.onclick = function() {
      const vote = this.dataset.vote;
      updateVotes(vote);
    }
  });
});

function updateVotes(vote) {
      
  // GET request to update_votes API route
  let post_id = vote.slice(4);
  url = `http://127.0.0.1:8000/update_votes/${post_id}`
  let headers = new Headers();
  headers.append('Access-Control-Allow-Origin', '*');
  headers.append('Content-Type', 'application/json');
  headers.append('Accept', 'application/json');
  fetch(url, {
    mode: 'cors',
    headers: headers,
  })
  
  .then(response => response.json())
  .then(result => {  
    console.log(result);
      document.querySelector(`#count_votes${post_id}`).innerHTML = result['votes_count'];    
  })
  .catch(error => console.log(error));
  return false;
}
