const INACTIVITY_LIMIT = 10 * 60 * 1000;
let inactivityTimer;

function resetTimer() {
    clearTimeout(inactivityTimer);

    inactivityTimer = setTimeout(() => {
        window.location.href = "/logout/";
    }, INACTIVITY_LIMIT);
}

document.addEventListener("mousemove", resetTimer);
document.addEventListener("click", resetTimer);
document.addEventListener("keydown", resetTimer);
document.addEventListener("scroll", resetTimer);
document.addEventListener("touchstart", resetTimer);

resetTimer();
