const images = [
    "FondoDash1.jpg",
    "FondoDash2.jpg",
];

function setRandomBackground() {
    const randomImage = images[Math.floor(Math.random() * images.length)];
    
    const mainContent = document.querySelector('.main-content');
    mainContent.style.backgroundImage = `url('images/${randomImage}')`;
    mainContent.style.backgroundSize = 'cover';        
    mainContent.style.backgroundPosition = 'center';   
    mainContent.style.backgroundRepeat = 'no-repeat';  
}

window.onload = setRandomBackground;
