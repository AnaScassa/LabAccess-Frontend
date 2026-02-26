export async function authFetch(url, options = {}) {
  let token = localStorage.getItem("access");

  if (!token) {
    throw new Error("Sem token");
  }

  let res = await fetch(url, {
    ...options,
    headers: {
      ...(options.headers || {}),
      Authorization: `Bearer ${token}`,
    },
  });

  if (res.status === 401 || res.status === 403) {
    const refresh = localStorage.getItem("refresh");

    if (!refresh) {
      throw new Error("Sem refresh token");
    }

    const refreshRes = await fetch(
      "http://localhost:8000/api/acesso/token/refresh/",
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ refresh }),
      }
    );

    if (!refreshRes.ok) {
      throw new Error("Refresh inválido");
    }

    const data = await refreshRes.json();
    localStorage.setItem("access", data.access);

    return fetch(url, {
      ...options,
      headers: {
        ...(options.headers || {}),
        Authorization: `Bearer ${data.access}`,
      },
    });
  }

  return res;
}
