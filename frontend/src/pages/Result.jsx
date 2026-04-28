import { useEffect, useState } from "react";
import API from "../services/api";

export default function Result() {
  const data = JSON.parse(localStorage.getItem("result"));
  const [articles, setArticles] = useState([]);

  console.log("RESULT DATA:", data);

    useEffect(() => {
    if (!data?.category) return;

    API.get(`/news/?category=${data.category}`)
        .then((res) => {
        setArticles(res.data.articles);
        })
        .catch((err) => {
        console.log(err);
        });
    }, [data?.category]);

  if (!data) return <p>Tidak ada data</p>;

  const getColor = (category) => {
    switch (category) {
      case "Minimal":
        return "green";
      case "Mild":
        return "orange";
      case "Moderate":
        return "gold";
      case "Severe":
        return "red";
      default:
        return "black";
    }
  };

  return (
    <div style={{ display: "flex", justifyContent: "center", marginTop: "50px" }}>
      <div
        style={{
          border: "1px solid #ccc",
          padding: "30px",
          borderRadius: "10px",
          width: "500px",
          boxShadow: "0 0 10px rgba(0,0,0,0.1)",
        }}
      >
        <h2>Hasil Evaluasi</h2>

        <h1 style={{ color: getColor(data.category) }}>
          {data.category}
        </h1>

        <p><strong>Total Score:</strong> {data.total_score}</p>

        <p style={{ marginTop: "10px" }}>
          {data.interpretation}
        </p>

        {/* 🔥 DETAIL PER PERTANYAAN */}
        <div style={{ marginTop: "20px" }}>
          <h3>Detail Jawaban</h3>

          {data.details.map((item, i) => (
            <div
              key={i}
              style={{
                borderTop: "1px solid #eee",
                paddingTop: "10px",
                marginTop: "10px",
              }}
            >
              <p><strong>Pertanyaan {i + 1}</strong></p>
              <p>Score: {item.score}</p>

              {item.text && (
                <p style={{ fontStyle: "italic" }}>
                  "{item.text}"
                </p>
              )}

              {/* 🔥 NLP INSIGHT */}
              {item.nlp && (
                <div style={{ fontSize: "12px", color: "gray" }}>
                  <p>Negative: {item.nlp.probabilities.negative.toFixed(2)}</p>
                  <p>Neutral: {item.nlp.probabilities.neutral.toFixed(2)}</p>
                  <p>Positive: {item.nlp.probabilities.positive.toFixed(2)}</p>
                </div>
              )}
            </div>
          ))}
        </div>

        {/* 📰 ARTIKEL */}
        <div style={{ marginTop: "20px" }}>
          <h3>Rekomendasi Artikel</h3>

          {articles.length === 0 ? (
            <p>Loading artikel...</p>
          ) : (
            articles.map((a, i) => (
              <div key={i} style={{ marginBottom: "10px" }}>
                <a href={a.url} target="_blank" rel="noreferrer">
                  <strong>{a.title}</strong>
                </a>
                <p style={{ fontSize: "12px", color: "gray" }}>
                  {a.description}
                </p>
              </div>
            ))
          )}
        </div>

        {/* 🔥 BUTTON */}
        <button
          onClick={() => (window.location.href = "/dashboard")}
          style={{ marginTop: "20px" }}
        >
          Cek Lagi
        </button>

        {/* DISCLAIMER */}
        <p style={{ fontSize: "12px", color: "gray", marginTop: "10px" }}>
          *Hasil ini bukan diagnosis medis, silakan konsultasi dengan profesional.
        </p>
      </div>
    </div>
  );
}