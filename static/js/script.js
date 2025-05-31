// static/js/script.js

// Wait for the DOM to fully load
document.addEventListener('DOMContentLoaded', function () {
    // Toggle between auto and manual inputs
    const manualRadio = document.getElementById('manual');
    const autoRadio = document.getElementById('auto');
    const manualInputs = document.getElementById('manual-inputs');

    function toggleManualInputs() {
        if (manualRadio && manualInputs && manualRadio.checked) {
            manualInputs.classList.remove('d-none');
        } else {
            manualInputs.classList.add('d-none');
        }
    }

    // Call on page load
    toggleManualInputs();

    // Listen for user switching between Auto and Manual modes
    if (manualRadio && autoRadio) {
        manualRadio.addEventListener('change', toggleManualInputs);
        autoRadio.addEventListener('change', toggleManualInputs);
    }

    // ---------- Motivational Quote Rotator ----------

    const quotes = [
        "Invest in yourself. Your career is the engine of your wealth.",
        "Financial freedom begins with a clear plan.",
        "A budget is telling your money where to go instead of wondering where it went.",
        "Saving is a great habit. Start today, enjoy tomorrow.",
        "Money is a tool. Use it wisely to build your future.",
        "Wealth grows when you invest in knowledge.",
        "Discipline in money matters leads to freedom in life.",
        "Your salary is your potential — maximize it with smart decisions."
    ];

    let currentQuoteIndex = 0;
    const quoteText = document.getElementById('quote-text');

    function showNextQuote() {
        if (!quoteText) return;

        // Fade out
        quoteText.style.opacity = 0;

        // Wait for fade-out transition, then switch quote and fade in
        setTimeout(() => {
            currentQuoteIndex = (currentQuoteIndex + 1) % quotes.length;
            quoteText.textContent = quotes[currentQuoteIndex];
            quoteText.style.opacity = 1;
        }, 500); // Match this with CSS transition time
    }

    setInterval(showNextQuote, 5000); // Rotate every 5 seconds
});
