import { useState } from "react";

export default function Chat({ backendUrl }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMessage = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput("");
    setLoading(true);

    try {
      const res = await fetch(`${backendUrl}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });
      const data = await res.json();
      const botMessage = { sender: "bot", text: data.reply || "No response" };
      setMessages((prev) => [...prev, botMessage]);
    } catch (err) {
      const botMessage = { sender: "bot", text: "Error connecting to backend." };
      setMessages((prev) => [...prev, botMessage]);
    }
    setLoading(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === "Enter") sendMessage();
  };

  return (
    <div style={{ maxWidth: 600, margin: "50px auto", fontFamily: "sans-serif" }}>
      <h2>Financial Chatbot</h2>
      <div
        style={{
          border: "1px solid #ccc",
          borderRadius: 8,
          padding: 10,
          minHeight: 400,
          maxHeight: 400,
          overflowY: "auto",
          marginBottom: 10,
        }}
      >
        {messages.map((msg, idx) => (
          <div
            key={idx}
            style={{
              textAlign: msg.sender === "user" ? "right" : "left",
              margin: "5px 0",
            }}
          >
            <span
              style={{
                display: "inline-block",
                padding: "8px 12px",
                borderRadius: 12,
                backgroundColor: msg.sender === "user" ? "#0b93f6" : "#e5e5ea",
                color: msg.sender === "user" ? "white" : "black",
              }}
            >
              {msg.text}
            </span>
          </div>
        ))}
        {loading && <div>Bot is typing...</div>}
      </div>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyDown={handleKeyPress}
        placeholder="Type your message..."
        style={{ width: "80%", padding: 8, marginRight: 5 }}
      />
      <button onClick={sendMessage} style={{ padding: "8px 12px" }}>
        Send
      </button>
    </div>
  );
}
