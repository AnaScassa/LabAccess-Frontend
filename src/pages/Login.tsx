import React, { useState } from "react";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [mensagem, setMensagem] = useState("");

  const handleLogin = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(
        "http://localhost:8000/api/acesso/login/",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({ username, password }),
        },
      );

      if (!response.ok) {
        setMensagem("Usuário ou senha inválidos");
        return;
      }

      const data = await response.json();

      console.log("ACCESS:", data.access);
      console.log("REFRESH:", data.refresh);

      localStorage.setItem("access", data.access);
      localStorage.setItem("refresh", data.refresh);

      console.log("LS ACCESS:", localStorage.getItem("access"));
      console.log("LS REFRESH:", localStorage.getItem("refresh"));

      window.location.replace("/upload");
    } catch (error) {
      console.error(error);
      setMensagem("Erro ao conectar com o servidor");
    }

  };

  return (
    <form onSubmit={handleLogin}>
      <input
        type="text"
        placeholder="Usuário"
        value={username}
        onChange={(e) => setUsername(e.target.value)}
      />

      <input
        type="password"
        placeholder="Senha"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
      />

      <button type="submit">Entrar</button>

      {mensagem && <p>{mensagem}</p>}
    </form>
  );
}
