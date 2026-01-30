import { useEffect, useState } from "react";

export default function App() {
  const [dashboard, setDashboard] = useState(null);

  useEffect(() => {
    fetch("/dashboard_ui.json")
      .then((res) => {
        if (!res.ok) {
          throw new Error("No se pudo cargar dashboard_ui.json");
        }
        return res.json();
      })
      .then((data) => {
        console.log("Dashboard cargado:", data);
        setDashboard(data);
      })
      .catch((err) => {
        console.error(err);
      });
  }, []);

  if (!dashboard) {
    return (
      <div className="min-h-screen flex items-center justify-center text-gray-600">
        Cargando dashboard generado por el agente...
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-100 p-10">
      <h1 className="text-4xl font-bold text-center mb-10">
        {dashboard.titulo}
      </h1>

      {/* KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
        {dashboard.kpis.map((kpi, i) => (
          <div
            key={i}
            className={`p-6 rounded-2xl text-white shadow-xl ${kpi.color}`}
          >
            <p className="text-sm opacity-80">{kpi.titulo}</p>
            <p className="text-4xl font-bold">{kpi.valor}</p>
          </div>
        ))}
      </div>

      {/* Secciones */}
      <div className="space-y-6">
        {dashboard.sections.map((s, i) => (
          <div
            key={i}
            className="bg-white p-6 rounded-xl shadow"
          >
            <h2 className="text-xl font-semibold mb-2">{s.titulo}</h2>
            <p className="text-gray-600">{s.descripcion}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
