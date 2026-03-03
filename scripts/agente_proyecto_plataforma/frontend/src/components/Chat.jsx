import { useState } from "react";

export default function Chat() {
  const [messages, setMessages] = useState([
    { role: "system", content: "Bienvenido Sube un archivo y pregunta lo que necesites." }
  ]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;

    setMessages([...messages, { role: "user", content: input }]);
    setInput("");

    const res = await fetch("http://127.0.0.1:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        message: input
      })

    });

    const data = await res.json();

    setMessages((prev) => [
      ...prev,
      { role: "assistant", content: data.response }
    ]);
  };

  return (
    <div style={{ padding: "1rem" }}>
      <div style={{ height: "60vh", overflowY: "auto", border: "1px solid #ccc", padding: "1rem" }}>
        {messages.map((m, i) => (
          <div key={i}>
            <strong>{m.role}:</strong> {m.content}
          </div>
        ))}
      </div>

      <div style={{ marginTop: "1rem" }}>
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          style={{ width: "80%" }}
        />
        <button onClick={sendMessage}>Enviar</button>
      </div>
    </div>
  );
}
