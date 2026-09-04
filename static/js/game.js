// === THE LAST EMBER - Game JavaScript ===

document.addEventListener('DOMContentLoaded', function() {
    initializeTypewriterEffect();
    initializeChoiceAnimations();
    initializeSmoothTransitions();
});

// Typewriter effect for story text
function initializeTypewriterEffect() {
    const paragraphs = document.querySelectorAll('.story-paragraph');
    
    paragraphs.forEach((paragraph, index) => {
        const originalText = paragraph.textContent;
        paragraph.textContent = '';
        paragraph.style.opacity = '0';
        
        setTimeout(() => {
            paragraph.style.opacity = '1';
            typeText(paragraph, originalText, 0);
        }, index * 500);
    });
}

function typeText(element, text, index) {
    if (index < text.length) {
        element.textContent += text.charAt(index);
        setTimeout(() => typeText(element, text, index + 1), 15);
    }
}

// Choice button animations
function initializeChoiceAnimations() {
    const choiceButtons = document.querySelectorAll('.choice-btn');
    
    choiceButtons.forEach((button, index) => {
        button.style.opacity = '0';
        button.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            button.style.transition = 'all 0.5s ease';
            button.style.opacity = '1';
            button.style.transform = 'translateY(0)';
        }, 1000 + (index * 200));
        
        // Add hover sound effect (visual feedback)
        button.addEventListener('mouseenter', function() {
            this.style.borderColor = 'var(--accent-orange)';
        });
        
        button.addEventListener('mouseleave', function() {
            this.style.borderColor = 'var(--border-color)';
        });
    });
}

// Smooth scene transitions
function initializeSmoothTransitions() {
    const choiceForm = document.getElementById('choice-form');
    
    if (choiceForm) {
        choiceForm.addEventListener('submit', function(e) {
            const selectedButton = document.activeElement;
            const allButtons = document.querySelectorAll('.choice-btn');
            
            // Fade out all content
            const storyPanel = document.querySelector('.story-panel');
            storyPanel.style.transition = 'opacity 0.5s ease';
            storyPanel.style.opacity = '0';
            
            // Highlight selected choice
            allButtons.forEach(btn => {
                if (btn !== selectedButton) {
                    btn.style.opacity = '0.3';
                } else {
                    btn.style.borderColor = 'var(--accent-orange)';
                    btn.style.background = 'rgba(212, 160, 82, 0.1)';
                }
            });
        });
    }
}

// Animate stat bars on page load
function animateStatBars() {
    const statFills = document.querySelectorAll('.stat-fill');
    
    statFills.forEach(fill => {
        const targetWidth = fill.style.width;
        fill.style.width = '0%';
        
        setTimeout(() => {
            fill.style.transition = 'width 1s ease-out';
            fill.style.width = targetWidth;
        }, 500);
    });
}

// Initialize stat bar animations
setTimeout(animateStatBars, 300);

// Add subtle parallax effect to floating embers
document.addEventListener('mousemove', function(e) {
    const embers = document.querySelectorAll('.ember');
    const mouseX = e.clientX / window.innerWidth;
    const mouseY = e.clientY / window.innerHeight;
    
    embers.forEach((ember, index) => {
        const speed = (index + 1) * 0.5;
        const xOffset = (mouseX - 0.5) * speed * 10;
        const yOffset = (mouseY - 0.5) * speed * 5;
        
        ember.style.transform = `translate(${xOffset}px, ${yOffset}px)`;
    });
});

// Keyboard navigation for choices
document.addEventListener('keydown', function(e) {
    const choiceButtons = document.querySelectorAll('.choice-btn');
    
    if (choiceButtons.length === 0) return;
    
    if (e.key === 'ArrowDown' || e.key === 'ArrowRight') {
        e.preventDefault();
        navigateChoices(1);
    } else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {
        e.preventDefault();
        navigateChoices(-1);
    }
});

let currentChoiceIndex = -1;

function navigateChoices(direction) {
    const choiceButtons = document.querySelectorAll('.choice-btn');
    
    if (choiceButtons.length === 0) return;
    
    // Remove highlight from current
    if (currentChoiceIndex >= 0 && currentChoiceIndex < choiceButtons.length) {
        choiceButtons[currentChoiceIndex].style.borderColor = 'var(--border-color)';
        choiceButtons[currentChoiceIndex].style.background = 'var(--bg-dark)';
    }
    
    // Move to next
    currentChoiceIndex += direction;
    
    if (currentChoiceIndex < 0) currentChoiceIndex = choiceButtons.length - 1;
    if (currentChoiceIndex >= choiceButtons.length) currentChoiceIndex = 0;
    
    // Highlight new choice
    const selectedButton = choiceButtons[currentChoiceIndex];
    selectedButton.style.borderColor = 'var(--accent-orange)';
    selectedButton.style.background = 'rgba(212, 160, 82, 0.1)';
    selectedButton.focus();
}

// Reset choice index when page loads
window.addEventListener('load', function() {
    currentChoiceIndex = -1;
});