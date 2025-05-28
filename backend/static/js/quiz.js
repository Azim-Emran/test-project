let startTime = Date.now();

function stopTimer() {
  const timeTaken = Math.floor((Date.now() - startTime) / 1000);
  document.getElementById("time_taken").value = timeTaken;
}
