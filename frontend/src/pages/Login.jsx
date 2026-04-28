import { useState } from "react";
import API from "../services/api";

export default function Login() {
  const [form, setForm] = useState({
    username: "",
    password: "",
    });

  const handleLogin = async () => {
    try {
      const res = await API.post("/auth/login/", form);

      localStorage.setItem("token", res.data.access);

      alert("Login berhasil!");
      window.location.href = "/dashboard";
    } catch (err) {
    console.log(err.response);
    alert(JSON.stringify(err.response?.data));
    }
  };

  return (
    <div>
      <h2>Login</h2>

    <input
        placeholder="Username"
        onChange={(e) =>
            setForm({ ...form, username: e.target.value })
        }
    />

      <input
        type="password"
        placeholder="Password"
        onChange={(e) =>
          setForm({ ...form, password: e.target.value })
        }
      />

      <button onClick={handleLogin}>Login</button>
    </div>
  );
}