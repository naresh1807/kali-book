// Pure policy function plus safe DOM output. No external resources or requests.
function acceptMessage(event, expectedOrigin, expectedSource) {
  return event.origin === expectedOrigin && event.source === expectedSource &&
    event.data !== null && typeof event.data === 'object' && !Array.isArray(event.data) &&
    event.data.type === 'lab-status' && typeof event.data.text === 'string' && event.data.text.length <= 80;
}
if (typeof document !== 'undefined') {
  document.getElementById('output').textContent = '<b>This stays text, not markup.</b>';
  // A self-message provides a controlled source for this standalone exercise.
  window.addEventListener('message', event => {
    if (acceptMessage(event, location.origin, window)) document.getElementById('output').textContent = event.data.text;
  });
}
if (typeof module !== 'undefined') module.exports = {acceptMessage};
