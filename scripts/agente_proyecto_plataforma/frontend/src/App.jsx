import Chat from "./components/Chat";

export default function App() {
  return (
    <div style={{ height: "100vh", fontFamily: "Arial, sans-serif" }}>
      <h2 style={{ textAlign: "center" }}>
        Plataforma Multiagente de Ciencia de Datos
      </h2>
      <Chat />
    </div>
  );
}
