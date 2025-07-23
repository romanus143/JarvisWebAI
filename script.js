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
