"use client";

import { useState, useEffect } from "react";

export default function Home() {
  const [message, setMessage] = useState("loading...");

  useEffect(() => {
    fetch("http://localhost:5000/api/ping")
      .then((res) => res.json())
      .then((data) => setMessage(data.message))
      .catch((err) => setMessage("Failed to connect to backend: " + err.message));
  }, []);

  return (
    <main style={{ padding: "40px", fontSize: "24px" }}>
      <h1>Gift App</h1>
      <p>Backend returned message: {message}</p>
    </main>
  );
}