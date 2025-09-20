import { useState } from "react";

export default function Chat() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const backendUrl = "https://fin-chatbot.onrender.com"; // your deployed backend

  const sendMessage = async () => {
    const payload = { user_id: "u1", message: input };

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
    <div>
      <div>
        {messages.map((m, i) => (
          <div key={i}>
            <b>You:</b> {m.user} <br />
            <b>Bot:</b> {m.bot}
          </div>
        ))}
      </div>
      <input value={input} onChange={(e) => setInput(e.target.value)} />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}
