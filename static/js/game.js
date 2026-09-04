// === THE LAST EMBER - Game JavaScript ===

document.addEventListener('DOMContentLoaded', function() {
    initializeTypewriterEffect();
    initializeSmoothTransitions();
    showStatChanges();
});

// Typewriter effect for story text - sequential from top to bottom
function initializeTypewriterEffect() {
    const paragraphs = document.querySelectorAll('.story-paragraph');
    const choicesContainer = document.getElementById('choices');
    
    // Hide choices container initially so decisions only appear after text animation
    if (choicesContainer) {
        choicesContainer.style.opacity = '0';
        choicesContainer.style.visibility = 'hidden';
    }
    
    // Store original text and clear all paragraphs
    const paragraphData = [];
    paragraphs.forEach((paragraph) => {
        const originalText = paragraph.textContent;
        paragraph.textContent = '';
        paragraph.style.opacity = '0';
        paragraphData.push({ element: paragraph, text: originalText });
    });
    
    // Track typing state
    let currentIndex = 0;
    let isTyping = false;
    let currentTimeout = null;
    let currentElement = null;
    let currentText = '';
    let currentOnComplete = null;
    
    // Click to skip current paragraph
    function handleSkipClick() {
        if (!isTyping) return;
        
        // Clear current typing timeout
        if (currentTimeout) {
            clearTimeout(currentTimeout);
        }
        
        // Instantly show all text for current paragraph
        if (currentElement && currentText) {
            currentElement.textContent = currentText;
            currentElement.innerHTML = parseMarkdown(currentElement.textContent);
        }
        
        // Reset typing state
        isTyping = false;
        currentElement = null;
        currentText = '';
        
        // Continue to next paragraph after short delay
        setTimeout(() => {
            if (currentOnComplete) {
                currentOnComplete();
            }
        }, 100);
    }
    
    // Add click listener
document.addEventListener('click', handleSkipClick);
    
    // Type paragraphs one at a time, waiting for each to finish
    function typeNextParagraph() {
        if (currentIndex >= paragraphData.length) {
            // All paragraphs finished, show choices and remove listener
            document.removeEventListener('click', handleSkipClick);
            initializeChoiceAnimations();
            return;
        }
        
        const { element, text } = paragraphData[currentIndex];
        currentIndex++;
        
        element.style.opacity = '1';
        isTyping = true;
        currentElement = element;
        currentText = text;
        currentOnComplete = typeNextParagraph;
        typeText(element, text, 0, typeNextParagraph);
    }
    
    // Start with the first paragraph
    typeNextParagraph();
}

function typeText(element, text, index, onComplete) {
    if (index < text.length) {
        element.textContent += text.charAt(index);
        // Store timeout so it can be cleared on skip
        element._timeout = setTimeout(() => typeText(element, text, index + 1, onComplete), 15);
    } else {
        // Current paragraph finished typing, render markdown to HTML
        element.innerHTML = parseMarkdown(element.textContent);
        // Move to next paragraph after a short pause
        setTimeout(onComplete, 300);
    }
}

// Simple markdown parser for story text formatting
function parseMarkdown(text) {
    let html = text;
    
    // Convert **bold** to <strong>
    html = html.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>');
    
    // Convert *italic* to <em> (but not inside already processed <strong> tags)
    html = html.replace(/\*(.+?)\*/g, '<em>$1</em>');
    
    // Convert --- to horizontal rule
    html = html.replace(/^---$/g, '<hr class="scene-divider">');
    
    return html;
}

// Choice button animations
function initializeChoiceAnimations() {
    const choicesContainer = document.getElementById('choices');
    const choiceButtons = document.querySelectorAll('.choice-btn');
    
    // Show choices container first after all text animation completes
    if (choicesContainer) {
        choicesContainer.style.transition = 'opacity 0.5s ease';
        choicesContainer.style.visibility = 'visible';
        choicesContainer.style.opacity = '1';
    }
    
    // Then animate each button with a stagger
    choiceButtons.forEach((button, index) => {
        button.style.opacity = '0';
        button.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            button.style.transition = 'all 0.5s ease';
            button.style.opacity = '1';
            button.style.transform = 'translateY(0)';
        }, 300 + (index * 200));
        
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

// Show floating stat change indicators
function showStatChanges() {
    const statsPanel = document.getElementById('stats-panel');
    const container = document.getElementById('stat-changes-container');

    if (!statsPanel || !container) return;

    // Get stat changes from data attribute
    let statChanges = {};
    try {
        statChanges = JSON.parse(statsPanel.dataset.statChanges || '{}');
    } catch (e) {
        return;
    }

    // If no changes, do nothing
    if (Object.keys(statChanges).length === 0) return;

    // Stat display names
    const statNames = {
        'hope': 'Hope',
        'guilt': 'Guilt',
        'resolve': 'Resolve'
    };

    // Create floating indicator for each changed stat
    Object.entries(statChanges).forEach(([stat, change], index) => {
        if (change === 0) return;

        const statElement = document.getElementById(`stat-${stat}`);
        if (!statElement) return;

        // Get position of the stat element
        const rect = statElement.getBoundingClientRect();

        // Create the floating indicator
        const indicator = document.createElement('div');
        indicator.className = `stat-change-indicator ${change > 0 ? 'positive' : 'negative'}`;
        indicator.textContent = change > 0 ? `+${change}` : `${change}`;

        // Position relative to the stat element
        indicator.style.position = 'fixed';
        indicator.style.left = `${rect.right + 10}px`;
        indicator.style.top = `${rect.top + rect.height / 2}px`;

        container.appendChild(indicator);

        // Trigger animation after a short delay
        setTimeout(() => {
            indicator.classList.add('show');
        }, 100 + (index * 150));

        // Remove indicator after animation completes
        setTimeout(() => {
            indicator.remove();
        }, 2000 + (index * 150));
    });
}
