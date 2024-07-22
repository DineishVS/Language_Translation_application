// Function to translate text
async function translateText() {
    const text = document.getElementById('inputText').value;
    const targetLang = document.getElementById('targetLang').value;

    try {
        const response = await fetch('/api/translate/text/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ text: text, target_lang: targetLang }),
        });
        const data = await response.json();
        document.getElementById('translatedText').textContent = data.translated_text;
        
        // Store translated text for playback
        window.translatedText = data.translated_text;
        window.translatedLang = targetLang;
    } catch (error) {
        console.error('Error translating text', error);
    }
}

// Function to start speech recognition
async function startSpeechRecognition() {
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    recognition.lang = 'en-US'; // Set language if needed
    recognition.interimResults = false;

    recognition.onresult = async function(event) {
        const transcript = event.results[0][0].transcript;
        document.getElementById('recognizedText').textContent = `Recognized Text: ${transcript}`;
        
        // Translate recognized text
        const targetLang = document.getElementById('targetLang').value;
        try {
            const response = await fetch('/api/translate/text/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ text: transcript, target_lang: targetLang }),
            });
            const data = await response.json();
            document.getElementById('translatedText').textContent = data.translated_text;
            
            // Store translated text for playback
            window.translatedText = data.translated_text;
            window.translatedLang = targetLang;
        } catch (error) {
            console.error('Error translating text', error);
        }
    };

    recognition.onerror = function(event) {
        console.error('Speech recognition error', event.error);
    };

    recognition.start();
}

// Function to play translated text
function playTranslatedText() {
    if (window.translatedText) {
        const utterance = new SpeechSynthesisUtterance(window.translatedText);
        utterance.lang = window.translatedLang || 'en';
        window.speechSynthesis.speak(utterance);
    } else {
        console.warn('No translated text available to play.');
    }
}
