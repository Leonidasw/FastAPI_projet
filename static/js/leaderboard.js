

  function formatScore(centiseconds) {
    const minutes = Math.floor(centiseconds / 6000);
    const seconds = Math.floor((centiseconds % 6000) / 100);
    const centis = centiseconds % 100;
    return `${minutes}:${seconds.toString().padStart(2, '0')}.${centis.toString().padStart(2, '0')}`;
};

window.onload = function() {

    const ham_button = document.querySelector('.hamburger');
    const get = document.querySelector(".navbar");
  
    ham_button.addEventListener('click', function (){
      ham_button.classList.toggle('is-active');
      get.classList.toggle('is-active');
    });
    // Get all rows in the first table except the header row
    const rows = document.querySelectorAll('table:first-of-type tbody tr');
    
    rows.forEach((row) => {
        // Get the Time column cell (3rd column; index 2)
        const timeCell = row.cells[2]; 
        if (timeCell) {
            const centiseconds = parseInt(timeCell.textContent.trim(), 10); // Parse text content as integer
            if (!isNaN(centiseconds)) { // Check if parsed value is valid
                timeCell.textContent = formatScore(centiseconds); // Update with formatted time
            }
        }
    });
};