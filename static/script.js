//first function start
window.addEventListener('scroll', function() {
    var tableHeader = document.querySelector('thead');
    var rect = tableHeader.getBoundingClientRect();
    
    if (rect.top <= 0) {
        tableHeader.classList.add('sticky');
    } else {
        tableHeader.classList.remove('sticky');
    }
});//first function end


// 1-20, -1 -20 color border function start
window.addEventListener('DOMContentLoaded', function() {
    var arbitrageCells = document.querySelectorAll('td.arbitrage');

    arbitrageCells.forEach(function(cell) {
        var arbitrage = parseFloat(cell.textContent);
        
        if (arbitrage >= 1 && arbitrage <= 20) {
            cell.classList.add('highlight-green');
        } else if (arbitrage >= -20 && arbitrage <= -1) {
            cell.classList.add('highlight-red');
        }
    });
});// 1-20, -1 -20 color border function end

//arrow key function start
window.addEventListener('DOMContentLoaded', function() {
    var arrowKey = document.getElementById('arrow-key');
    var greenCells = document.querySelectorAll('td.highlight-green');
    var redCells = document.querySelectorAll('td.highlight-red');

    var currentIndex = -1;
    var clickCount = 0;

    arrowKey.addEventListener('click', function() {
        clickCount++;

        if (clickCount === 1) {
            if (currentIndex === -1 || currentIndex === greenCells.length - 1) {
                currentIndex = 0;
            } else {
                currentIndex++;
            }

            if (greenCells.length > 0) {
                greenCells.forEach(function(cell) {
                    cell.classList.remove('current');
                });

                greenCells[currentIndex].classList.add('current');
                greenCells[currentIndex].scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        } else if (clickCount === 2) {
            if (currentIndex === -1 || currentIndex === redCells.length - 1) {
                currentIndex = 0;
            } else {
                currentIndex++;
            }

            if (redCells.length > 0) {
                redCells.forEach(function(cell) {
                    cell.classList.remove('current');
                });

                redCells[currentIndex].classList.add('current');
                redCells[currentIndex].scrollIntoView({ behavior: 'smooth', block: 'center' });
            }
        } else {
            window.scrollTo({ top: 0, behavior: 'smooth' });
            clickCount = 0;
        }
    });
});// arrow key function end

//selection function start

document.addEventListener('DOMContentLoaded', function() {
  // Select cells and rows
  var cells = document.querySelectorAll('td, th');
  var rows = document.querySelectorAll('tr');

  // Initialize variables
  var isArtMode = false;
  var selectedColor = '#ff0000';
  var lastClickedElement = null;

  // Add event listeners to cells and rows
  cells.forEach(function (cell) {
    cell.addEventListener('click', handleCellClick);
  });

  rows.forEach(function (row) {
    row.addEventListener('click', handleRowClick);
  });

  // Handle cell click event
  function handleCellClick(event) {
    if (isArtMode) {
      event.target.style.backgroundColor = selectedColor;
      lastClickedElement = null;
    } else {
      if (event.target.classList.contains('highlighted')) {
        event.target.classList.remove('highlighted');
        lastClickedElement = null;
      } else {
        if (lastClickedElement) {
          lastClickedElement.classList.remove('highlighted');
        }
        event.target.classList.add('highlighted');
        lastClickedElement = event.target;
      }
    }
  }

  // Handle row click event
  function handleRowClick(event) {
    if (isArtMode) {
      var cells = event.currentTarget.querySelectorAll('td, th');
      cells.forEach(function (cell) {
        cell.style.backgroundColor = selectedColor;
      });
      lastClickedElement = null;
    } else {
      if (event.currentTarget.classList.contains('highlighted')) {
        event.currentTarget.classList.remove('highlighted');
        lastClickedElement = null;
      } else {
        if (lastClickedElement) {
          lastClickedElement.classList.remove('highlighted');
        }
        event.currentTarget.classList.add('highlighted');
        lastClickedElement = event.currentTarget;
      }
    }
  }

  // Handle color picker change event
  var colorPicker = document.getElementById('selected-color');
  colorPicker.addEventListener('input', function (event) {
    selectedColor = event.target.value;
  });

  // Toggle art mode
  var colorPickerDiv = document.getElementById('color-picker');
  colorPickerDiv.addEventListener('click', function () {
    isArtMode = !isArtMode;
    colorPickerDiv.classList.toggle('art-mode');
    if (lastClickedElement) {
      lastClickedElement.classList.remove('highlighted');
      lastClickedElement = null;
    }
  });
});//color selection end

document.addEventListener("DOMContentLoaded", function() {
  const coinSelect = document.getElementById("coin-select");
  
  // Example coin options, you can replace these with your actual coin list
  const coins = ["Bitcoin", "Ethereum", "Cardano", "Solana"];
  
  coins.forEach(coin => {
    const option = document.createElement("option");
    option.value = coin.toLowerCase(); // Use lowercase for value
    option.textContent = coin;
    coinSelect.appendChild(option);
  });
});


