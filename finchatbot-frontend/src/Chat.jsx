import { useState } from "react";

export default function Chat() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const backendUrl = "https://fin-chatbot.onrender.com";

  const sendMessage = async () => {
    if (!input.trim()) return;

    const payload = { message: input };

    try {
      const res = await fetch(`${backendUrl}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      });
      
      const data = await res.json();
      setMessages([...messages, { user: input, bot: data.reply }]);
      setInput("");
    } catch (err) {
      console.error("Error sending message:", err);
    }
  };

  return (
    <div style={{ maxWidth: "600px", margin: "50px auto", fontFamily: "Arial" }}>
      <h2 style={{ textAlign: "center" }}>💰 Financial Assistant</h2>
      <div style={{ border: "1px solid #ccc", borderRadius: "8px", padding: "10px", height: "400px", overflowY: "auto", marginBottom: "10px" }}>
        {messages.map((m, i) => (
          <div key={i} style={{ marginBottom: "15px" }}>
            <div style={{ textAlign: "right", color: "#007bff" }}><b>You:</b> {m.user}</div>
            <div style={{ textAlign: "left", color: "#28a745" }}><b>Bot:</b> {m.bot}</div>
          </div>
        ))}
      </div>
      <div style={{ display: "flex" }}>
        <input
          style={{ flex: 1, padding: "10px", borderRadius: "8px 0 0 8px", border: "1px solid #ccc" }}
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Type your message..."
        />
        <button
          onClick={sendMessage}
          style={{ padding: "10px 20px", border: "none", backgroundColor: "#007bff", color: "#fff", borderRadius: "0 8px 8px 0" }}
        >
          Send
        </button>
      </div>
    </div>
  );
}
