import { Routes, Route } from "react-router-dom";
import Upload from "./pages/Upload";
import Listagem from "./pages/Listagem";
import Usuarios from "./pages/Usuarios";
import TempoPermanencia from "./pages/TempoPermanencia";
import Login from "./pages/Login";

export default function App() {
  return (
    <Routes>
      <Route path="/upload" element={<Upload />} />
      <Route path="/listagem" element={<Listagem />} />
      <Route path="/usuarios" element={<Usuarios />} />
      <Route path="/tempoPermanencia" element={<TempoPermanencia />} />
      <Route path="/login" element={<Login />} />
    </Routes>
  );
}
