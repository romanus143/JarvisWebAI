async function sendQuery(input = null) {
  console.log("Sending query...");

  const query = input || document.getElementById("query").value;
  if (!query.trim()) {
    document.getElementById("response").innerText = "Please enter a question.";
    return;
  }

  try {
    const res = await fetch("https://jarviswebai.onrender.com/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: query })
    });

    const data = await res.json();
    console.log("Raw response:", data);

    const reply = data.response || "No response received.";
    document.getElementById("response").innerText = reply;
    speak(reply);
  } catch (err) {
    console.error("Error:", err);
    document.getElementById("response").innerText = "⚠️ Something went wrong while contacting Baba.";
  }
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
      setTimeout(loadVoices, 100);
    }
  };

  if (synth.onvoiceschanged !== undefined) {
    synth.onvoiceschanged = loadVoices;
  } else {
    loadVoices();
  }
}

function startListening() {
  const recognition = new webkitSpeechRecognition();
  recognition.lang = "en-US";

  recognition.onresult = (event) => {
    const voiceInput = event.results[0][0].transcript;
    document.getElementById("query").value = voiceInput;
    sendQuery(voiceInput);
  };

  recognition.onerror = (event) => {
    console.error("Speech recognition error:", event.error);
    document.getElementById("response").innerText = "⚠️ Voice input failed. Try typing your question.";
  };

  recognition.start();
}
