// script.js
async function sendQuery(input = null) {
  const query = input || document.getElementById("query").value;
  const res = await fetch("https://jarviswebai.onrender.com/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query: query })
  });
  const data = await res.json();
  document.getElementById("response").innerText = data.response;
  speak(data.response);
}

function speak(text) {
  const synth = window.speechSynthesis;
  const utter = new SpeechSynthesisUtterance(text);
  synth.speak(utter);
}

function startListening() {
  const recognition = new webkitSpeechRecognition();
  recognition.lang = "en-US";
  recognition.onresult = (e) => {
    const voiceInput = e.results[0][0].transcript;
    sendQuery(voiceInput);
  };
  recognition.start();
}
function speak(text) {
  const synth = window.speechSynthesis;
  const utter = new SpeechSynthesisUtterance(text);

  const loadVoices = () => {
    const voices = synth.getVoices();
    if (voices.length > 0) {
      utter.voice = voices.find(v => v.lang === "en-US") || voices[0];
      synth.speak(utter);
    } else {
      // Retry after a short delay
      setTimeout(loadVoices, 100);
    }
  };

  // Wait for voices to load
  if (synth.onvoiceschanged !== undefined) {
    synth.onvoiceschanged = loadVoices;
  } else {
    loadVoices();
  }
}

