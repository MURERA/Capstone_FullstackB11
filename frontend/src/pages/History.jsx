import { useEffect, useState } from "react";
import API from "../services/api";
import Navbar from "../components/Navbar";

export default function History() {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    API.get("/history/")
      .then((res) => {
        setHistory(res.data);
      })
      .catch((err) => {
        console.log(err.response);
      });
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      {/* 🔥 NAVBAR */}
      <Navbar />

      {/* 🔥 CONTENT */}
      <div style={{ padding: "20px" }}></div> 
      <h2>Riwayat Pemeriksaan</h2>

      {history.length === 0 ? (
        <p>Belum ada data</p>
      ) : (
        history.map((item, i) => (
          <div
            key={i}
            style={{
              border: "1px solid #ccc",
              padding: "15px",
              marginTop: "10px",
              borderRadius: "8px",
            }}
          >
            <p><strong>Kategori:</strong> {item.category}</p>
            <p><strong>Score:</strong> {item.total_score}</p>
            <p style={{ fontSize: "12px", color: "gray" }}>
              {new Date(item.created_at).toLocaleString()}
            </p>
          </div>
        ))
      )}
    </div>
  );
}