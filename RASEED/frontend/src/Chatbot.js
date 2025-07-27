import React, { useState } from 'react';
import './Chatbot.css';

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { text: 'Hi! How can I assist you today?\nPlease select your language:', sender: 'bot' }
  ]);
  const [userInput, setUserInput] = useState('');
  const [language, setLanguage] = useState('');

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const languageNames = {
    en: 'English',
    es: 'Spanish',
    fr: 'French',
    hi: 'Hindi',
    de: 'German',
    zh: 'Chinese'
  };

  const handleLanguageSelection = (langCode) => {
    setLanguage(langCode);
    // Clear previous messages except the first welcome message
    const welcomeMessage = messages[0];
    const assistanceText = translateAssistance('How can I assist you further?', langCode);
    
    setMessages([
      welcomeMessage,
      { text: `${languageNames[langCode]} selected. ${assistanceText}`, sender: 'bot' }
    ]);
  };

  const handleUserMessage = async (message) => {
    if (message.trim() === '') return;
    setMessages([...messages, { text: message, sender: 'user' }]);
    setUserInput('');
    if (!language) {
      handleLanguageSelection(message);
    } else {
      // Send all questions to the backend dietary coaching endpoint
      try {
        const res = await fetch('/api/dietary-coaching', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ query: message })
        });
        const data = await res.json();
        
        // Translate the response to the selected language
        let translatedResponse = data.response;
        if (language !== 'en') {
          try {
            // In a production app, you would call a translation API here
            // For now, we'll simulate translation with our basic translations
            translatedResponse = await translateWithAPI(data.response, language);
          } catch (err) {
            console.error('Translation failed:', err);
            // Fall back to original response if translation fails
          }
        }
        
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: translatedResponse, sender: 'bot' }
        ]);
      } catch (e) {
        const errorMsg = "Sorry, I couldn't fetch a response.";
        const translatedError = language === 'en' ? errorMsg : translateErrorMessage(errorMsg, language);
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: translatedError, sender: 'bot' }
        ]);
      }
    }
  };

  const formatMessage = (text) => {
    if (!text) return '';
    
    // Convert asterisks to bold
    let formattedText = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    formattedText = formattedText.replace(/\*(.*?)\*/g, '<strong>$1</strong>');
    
    // Convert bullet points
    formattedText = formattedText.replace(/^\s*[-•]\s+(.+)$/gm, '<li>$1</li>');
    formattedText = formattedText.replace(/(<li>.*?<\/li>)/gs, '<ul>$1</ul>');
    
    // Convert line breaks to paragraphs
    formattedText = formattedText.replace(/\n\n/g, '</p><p>');
    formattedText = `<p>${formattedText}</p>`;
    
    // Fix any nested paragraph tags
    formattedText = formattedText.replace(/<p><ul>/g, '<ul>');
    formattedText = formattedText.replace(/<\/ul><\/p>/g, '</ul>');
    
    return formattedText;
  };

  // Translation functions
  const translateAssistance = (text, lang) => {
    const translations = {
      en: text,
      es: '¿Cómo puedo ayudarte más?',
      fr: 'Comment puis-je vous aider davantage?',
      hi: 'मैं आपकी आगे कैसे मदद कर सकता हूँ?',
      de: 'Wie kann ich Ihnen weiterhelfen?',
      zh: '我能为您提供什么帮助？'
    };
    return translations[lang] || text;
  };

  const translateFollowUp = (text, lang) => {
    const translations = {
      en: text,
      es: '¿Qué más te gustaría saber?',
      fr: 'Que souhaitez-vous savoir d\'autre?',
      hi: 'आप और क्या जानना चाहेंगे?',
      de: 'Was möchten Sie sonst noch wissen?',
      zh: '您还想了解什么？'
    };
    return translations[lang] || text;
  };

  // Translate error messages
  const translateErrorMessage = (text, lang) => {
    const translations = {
      en: text,
      es: "Lo siento, no pude obtener una respuesta.",
      fr: "Désolé, je n'ai pas pu obtenir de réponse.",
      hi: "क्षमा करें, मैं प्रतिक्रिया प्राप्त नहीं कर सका।",
      de: "Entschuldigung, ich konnte keine Antwort abrufen.",
      zh: "抱歉，我无法获取回复。"
    };
    return translations[lang] || text;
  };

  // Simulate API translation (in a production app, this would call a translation API)
  const translateWithAPI = async (text, lang) => {
    // For demo purposes, we'll use a simple mapping for common phrases
    // In a real app, you would use a translation API like Google Translate
    
    // Wait a moment to simulate API call
    await new Promise(resolve => setTimeout(resolve, 300));
    
    // If English or no text, return as is
    if (lang === 'en' || !text) return text;
    
    // Spanish translations
    if (lang === 'es') {
      return text
        .replace(/Hello|Hi/gi, 'Hola')
        .replace(/Thank you|Thanks/gi, 'Gracias')
        .replace(/Here are some suggestions/gi, 'Aquí hay algunas sugerencias')
        .replace(/You can/gi, 'Puedes')
        .replace(/Try/gi, 'Intenta')
        .replace(/Consider/gi, 'Considera')
        .replace(/based on your/gi, 'basado en tus')
        .replace(/purchases/gi, 'compras')
        .replace(/healthy vegetables/gi, 'vegetales saludables')
        .replace(/you could/gi, 'podrías')
        .replace(/easily incorporate/gi, 'incorporar fácilmente')
        .replace(/into your diet/gi, 'en tu dieta')
        .replace(/Leafy Greens/gi, 'Verduras de Hoja Verde')
        .replace(/Spinach/gi, 'Espinaca')
        .replace(/kale/gi, 'col rizada')
        .replace(/can be added to/gi, 'se puede añadir a')
        .replace(/smoothies/gi, 'batidos')
        .replace(/you already buy/gi, 'ya compras')
        .replace(/or used in/gi, 'o usado en')
        .replace(/salads/gi, 'ensaladas')
        .replace(/Broccoli/gi, 'Brócoli')
        .replace(/Cauliflower/gi, 'Coliflor')
        .replace(/Great/gi, 'Excelente')
        .replace(/roasted/gi, 'asado')
        .replace(/steamed/gi, 'al vapor')
        .replace(/as a side dish/gi, 'como guarnición')
        .replace(/Carrots/gi, 'Zanahorias')
        .replace(/Easy to snack on/gi, 'Fáciles de comer como aperitivo')
        .replace(/relatively inexpensive/gi, 'relativamente baratas')
        .replace(/Okay/gi, 'Bien');
    }
    
    // French translations
    if (lang === 'fr') {
      return text
        .replace(/Hello|Hi/gi, 'Bonjour')
        .replace(/Thank you|Thanks/gi, 'Merci')
        .replace(/Here are some suggestions/gi, 'Voici quelques suggestions')
        .replace(/You can/gi, 'Vous pouvez')
        .replace(/Try/gi, 'Essayez')
        .replace(/Consider/gi, 'Considérez')
        .replace(/based on your/gi, 'selon vos')
        .replace(/purchases/gi, 'achats')
        .replace(/healthy vegetables/gi, 'légumes sains')
        .replace(/you could/gi, 'vous pourriez')
        .replace(/easily incorporate/gi, 'facilement incorporer')
        .replace(/into your diet/gi, 'dans votre alimentation')
        .replace(/Leafy Greens/gi, 'Légumes à Feuilles')
        .replace(/Spinach/gi, 'Épinards')
        .replace(/kale/gi, 'chou frisé')
        .replace(/can be added to/gi, 'peuvent être ajoutés à')
        .replace(/smoothies/gi, 'smoothies')
        .replace(/you already buy/gi, 'vous achetez déjà')
        .replace(/or used in/gi, 'ou utilisés dans')
        .replace(/salads/gi, 'salades')
        .replace(/Broccoli/gi, 'Brocoli')
        .replace(/Cauliflower/gi, 'Chou-fleur')
        .replace(/Great/gi, 'Excellent')
        .replace(/roasted/gi, 'rôti')
        .replace(/steamed/gi, 'cuit à la vapeur')
        .replace(/as a side dish/gi, 'comme accompagnement')
        .replace(/Carrots/gi, 'Carottes')
        .replace(/Easy to snack on/gi, 'Faciles à grignoter')
        .replace(/relatively inexpensive/gi, 'relativement peu coûteuses')
        .replace(/Okay/gi, 'D\'accord');
    }
    
    // German translations
    if (lang === 'de') {
      return text
        .replace(/Hello|Hi/gi, 'Hallo')
        .replace(/Thank you|Thanks/gi, 'Danke')
        .replace(/Here are some suggestions/gi, 'Hier sind einige Vorschläge')
        .replace(/You can/gi, 'Sie können')
        .replace(/Try/gi, 'Versuchen Sie')
        .replace(/Consider/gi, 'Erwägen Sie')
        .replace(/based on your/gi, 'basierend auf Ihren')
        .replace(/purchases/gi, 'Einkäufen')
        .replace(/healthy vegetables/gi, 'gesundes Gemüse')
        .replace(/you could/gi, 'könnten Sie')
        .replace(/easily incorporate/gi, 'leicht integrieren')
        .replace(/into your diet/gi, 'in Ihre Ernährung')
        .replace(/Leafy Greens/gi, 'Blattgemüse')
        .replace(/Spinach/gi, 'Spinat')
        .replace(/kale/gi, 'Grünkohl')
        .replace(/can be added to/gi, 'kann hinzugefügt werden zu')
        .replace(/smoothies/gi, 'Smoothies')
        .replace(/you already buy/gi, 'Sie kaufen bereits')
        .replace(/or used in/gi, 'oder verwendet in')
        .replace(/salads/gi, 'Salaten')
        .replace(/Broccoli/gi, 'Brokkoli')
        .replace(/Cauliflower/gi, 'Blumenkohl')
        .replace(/Great/gi, 'Großartig')
        .replace(/roasted/gi, 'geröstet')
        .replace(/steamed/gi, 'gedämpft')
        .replace(/as a side dish/gi, 'als Beilage')
        .replace(/Carrots/gi, 'Karotten')
        .replace(/Easy to snack on/gi, 'Leicht zu snacken')
        .replace(/relatively inexpensive/gi, 'relativ günstig')
        .replace(/Okay/gi, 'In Ordnung');
    }
    
    // Hindi translations
    if (lang === 'hi') {
      return text
        .replace(/Hello|Hi/gi, 'नमस्ते')
        .replace(/Thank you|Thanks/gi, 'धन्यवाद')
        .replace(/Here are some suggestions/gi, 'यहां कुछ सुझाव हैं')
        .replace(/You can/gi, 'आप कर सकते हैं')
        .replace(/Try/gi, 'प्रयास करें')
        .replace(/Consider/gi, 'विचार करें');
    }
    
    // Chinese translations
    if (lang === 'zh') {
      return text
        .replace(/Hello|Hi/gi, '你好')
        .replace(/Thank you|Thanks/gi, '谢谢')
        .replace(/Here are some suggestions/gi, '这里有一些建议')
        .replace(/You can/gi, '您可以')
        .replace(/Try/gi, '尝试')
        .replace(/Consider/gi, '考虑');
    }
    
    // Default: return original text
    return text;
  };

  const handleInputChange = (e) => {
    setUserInput(e.target.value);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleUserMessage(userInput);
    }
  };

  return (
    <div className="chatbot">
      <button className="chat-button" onClick={toggleChat}>
        {isOpen ? '×' : '💬'}
      </button>
      {isOpen && (
        <div className="chat-window">
          <div className="chat-header">
            <span>Raseed AI Assistant</span>
            <button onClick={toggleChat} style={{ background: 'none', border: 'none', color: 'white', cursor: 'pointer' }}>×</button>
          </div>
          <div className="chat-body">
            {messages.map((msg, index) => (
              <div key={index} className={`chat-message ${msg.sender}`}>
                <div className="avatar">{msg.sender === 'bot' ? '👨‍💼' : '👤'}</div>
                <div 
                  className="message" 
                  dangerouslySetInnerHTML={{ __html: formatMessage(msg.text) }}
                />
              </div>
            ))}
            {!language && (
              <div className="language-options">
                {Object.keys(languageNames).map((code) => (
                  <button
                    key={code}
                    className="language-button"
                    onClick={() => handleLanguageSelection(code)}
                  >
                    {languageNames[code]}
                  </button>
                ))}
              </div>
            )}
            {language && (
              <button
                className="change-language-button"
                onClick={() => setLanguage('')}
              >
                Change Language
              </button>
            )}
          </div>
          <div className="chat-input">
            <input
              type="text"
              value={userInput}
              onChange={handleInputChange}
              onKeyPress={handleKeyPress}
              placeholder="Type your message..."
            />
            <button className="send-button" onClick={() => handleUserMessage(userInput)}>➤</button>
          </div>
        </div>
      )}
    </div>
  );
};

export default Chatbot;